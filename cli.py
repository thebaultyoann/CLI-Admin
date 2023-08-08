import typer
from functools import wraps
from typing_extensions import Annotated
from passlib.context import CryptContext
import os
import time
import datetime
import threading
import database

app = typer.Typer()
user_app = typer.Typer()
app.add_typer(user_app, name="user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

database_name = "espf_users"
container_name = "mariadb"

#Wrapper used to check the user connexion
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        name=os.getenv('name')  
        password=os.getenv('password')
        if user_authentificated(name=name,password=password):
            return function(*args, **kwargs)
        else:
            return typer.secho(f"Wrong credentials", fg=typer.colors.RED)
    return wrapper

#Function used to check the credentials on a specific route
def user_authentificated(name:str, password:str):
    if name==None or password==None:
        typer.secho(f"You need to login", fg=typer.colors.RED)
        return False
    password = get_password_hash(password) #2nd hash of the admin password used to connect to the DB
    try: 
        global database_name
        global container_name
        database.test_credentials(
            DB_Username_For_Admin=name,
            DB_Password_For_Admin=password,
            DB_Name_For_Users_Tables=database_name,
            DB_Container_Name=container_name
        )   
    except:
        return False
    return True

################ ALL OF THE CLI COMMANDS ################

@app.command("login")
def login(
    username: Annotated[str, typer.Option(prompt=True)], 
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)]
    ) -> None: 
    password = get_password_hash(password)  #1st hash of the admin password stored in an env variable
    if user_authentificated(username=username, password=password):
        os.putenv('username',f'{username}')
        os.putenv('password',f'{password}')
        background_thread = threading.Thread(target=auto_logout)
        background_thread.start()
        typer.secho(f"You are now connected", fg=typer.colors.GREEN)
        return os.system('bash')
    else:
        os.putenv('username','')
        os.putenv('password','')
        typer.secho(f"Wrong credentials", fg=typer.colors.RED)
        return os.system('bash')

@app.command("logout")
def logout() -> None: 
        os.putenv('username','')
        os.putenv('password','')
        typer.secho(f"You are now disconnected", fg=typer.colors.RED)
        return os.system('bash')

@user_app.command("list")
@login_required
def user() -> None:
    session = connect_to_db()
    user_list(session=session)

@user_app.command('add')
@login_required
def user_add_command(
    username:str, 
    password: Annotated[str, typer.Option(prompt="The client password", hide_input=True)], 
    disabled: Annotated[bool, typer.Argument()]=False
    ) -> None:
    session = connect_to_db()
    user_add(session=session, username=username, password=password, disabled=disabled)
        
@user_app.command("get")
@login_required
def user_get_command(username:str) -> None:
    session = connect_to_db()
    user_get(session=session, username=username)

@user_app.command("delete")
@login_required
def user_delete_command(username:str) -> None:
    session = connect_to_db()
    user_delete(session=session, username=username)

@user_app.command('update')
@login_required
def user_update_command(
    username:str, 
    newUsername:Annotated[str, typer.Option(
            "--newusername",
            "-u")
        ]=None,
    newPassword: Annotated[str, typer.Option(
            "--newpassword",
            "-pw",
            hide_input=True)
        ]=None, 
    deactivate: Annotated[bool, typer.Option(
            "--deactivate/--activate",
            "-d/-a")
        ]=None,
    expirationDate : Annotated[str, typer.Option(
            "--expirationdate",
            "-expd")
        ]=None
    ) -> None:
    session = connect_to_db()
    user_update(session=session, username=username, newUsername = newUsername, password=newPassword, disabled=deactivate, expirationDate=expirationDate)
        
@user_app.command('activate')
@login_required
def user_activate_command(username:str) -> None:
    session = connect_to_db()
    user_activate(session=session, username=username)

@user_app.command('deactivate')
@login_required
def user_deactivate_command(username:str) -> None:
    session = connect_to_db()
    user_deactivate(session=session, username=username)

@user_app.command('changedate')
@login_required
def user_change_expiration_date(
    username:str,
    expirationDate: Annotated[str, typer.Argument(help="The expiration date for the user, format: dd/mm/yyyy")]
    ) -> None:
    session = connect_to_db()
    expirationDate=convert_string_to_date(date=expirationDate)
    if expirationDate:
        user_change_expiration_date(session=session, username=username, expirationDate=expirationDate)
    else:
        typer.secho(f"Wrong format for expiration date", fg=typer.colors.RED)

################ FUNCTIONS USED TO LIGHTEN CLI COMMANDS CODE ################

def user_list(session):
    users = database.get_all_users(session)
    if len(users) == 0:
        typer.secho("There are no users in the database yet", fg=typer.colors.RED)
        raise typer.Exit()
    typer.secho("\nUser list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Username  ",
        "| Disabled  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, user in enumerate(users, 1):
        username, disabled = user.username, user.disabled
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({username}){(len(columns[1]) - len(str(username)) - 4) * ' '}"
            f"| {disabled}{(len(columns[2]) - len(str(disabled)) - 2) * ' '}",   
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
    return True

def user_add(session, username:str, password:str, disabled:bool):
    password = get_password_hash(password)
    if database.add_user(session=session, username=username, password=password, disabled=disabled):
        return typer.secho(f"User {username} was added to the database and his disabled state is {disabled}", fg=typer.colors.GREEN)
    return typer.secho(f"Unsuccesfull add of the user {username}", fg=typer.colors.RED)

def user_get(session, username:str):
    user = database.get_a_single_user(session=session, username=username)
    if not user:
        typer.secho("This user doesn't exist", fg=typer.colors.RED)
        raise typer.Exit()
    typer.secho("\nUser:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Username  ",
        "| Disabled  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    id, username, disabled = user.id, user.username, user.disabled
    typer.secho(
        f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
        f"| ({username}){(len(columns[1]) - len(str(username)) - 4) * ' '}"
        f"| {disabled}{(len(columns[2]) - len(str(disabled)) - 2) * ' '}",   
        fg=typer.colors.BLUE,
    )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
    return True

def user_delete(session, username:str):
    user = database.get_a_single_user(session=session, username=username)
    if user:
        if ask_confirmation_delete_user:
            user = database.delete_user(session=session, username=username)
            typer.secho(f"User {user.username} have been delete", fg=typer.color.GREEN)
        else : 
            typer.secho(f"Deletion of {user.username} cancelled", fg=typer.colors.RED)
    else: 
        typer.secho("This user doesn't exist", fg=typer.colors.RED)

def user_update(session, username:str, newUsername:str, password:str,  disabled:bool, expirationDate:datetime.date):
    password = get_password_hash(password)
    code = database.update_user(session=session, username=username, newUsername=newUsername, password=password, disabled=disabled, expirationDate=expirationDate)
    if "1" in code :
        typer.secho(f"User {username} disabled state is now {disabled}", fg=typer.colors.GREEN)
    if "2" in code : 
        typer.secho(f"User {username} password has been changed", fg=typer.colors.GREEN)
    if "3" in code :  
        typer.secho(f"User {username} is now {newUsername}", fg=typer.colors.GREEN)
    if "4" in code :
        typer.secho(f"User {username} expiration date is now {expirationDate}")
    if "5" in code : 
        typer.secho(f"User {username} the new expiration date is before the old expiration date. If you want to perform this operation use the command changedate")
    if not ("1" in code or "2" in code or "3" in code or "4" in code or "5" in code) :
        typer.secho(f"Unsuccesfull modficiation of the user {username}", fg=typer.colors.RED)
 
def user_activate(session, username:str):
    if database.activate_user(session=session, username=username):
        return typer.secho(f"User {username} was activated")
    return typer.secho(f"Unsuccesfull activation of the user {username}", fg=typer.colors.RED)

def user_deactivate(session, username:str):
    if database.deactivate_user(session=session, username=username):
        return typer.secho(f"User {username} was deactivated")
    return typer.secho(f"Unsuccesfull deactivation of the user {username}", fg=typer.colors.RED)

def user_change_expiration_date(session, username:str, expirationDate:datetime.date):
    if not database.check_expiration_date(session=session, username=username, expirationDate=expirationDate):
        if ask_confirmation_expiration_date(expirationDate):
            database.change_expiration_date(session=session, username=username, expirationDate=expirationDate)
            typer.secho(f"User {user.username} expiration date is now {expirationDate}", fg=typer.color.GREEN)
        else:
            typer.secho("Modification of expiration date cancelled", fg=typer.colors.RED)
            return False
    else: 
        database.change_expiration_date(session=session, username=username, expirationDate=expirationDate)
        typer.secho(f"User {user.username} expiration date is now {expirationDate}", fg=typer.color.GREEN)
        return True

################ UTITLY FUNCTIONS ################

def convert_string_to_date(date_string):
    try:
        day, month, year = map(int, date_string.split('/'))
        new_date = datetime.date(year, month, day)
        if new_date.year == year and new_date.month == month and new_date.day == day:
            return new_date
        else:
            return None
    except (ValueError, AttributeError):
        return None
    except:
        return None
    
def ask_confirmation_expiration_date(expirationDate):
    confirmed = False
    valid_responses = {'yes', 'no'}
    while not confirmed:
        user_input = input(f"You are going to update to an expiration date which is closer than the actual one : {expirationDate}, do you confirm (yes/no): ").lower()
        if user_input in valid_responses:
            if user_input == 'yes':
                confirmed = True
            else:
                return False
        else:
            print("Invalid response. Answer with 'yes' ou 'no'.")
    return True

def ask_confirmation_delete_user(username):
    confirmed = False
    valid_responses = {'yes', 'no'}
    while not confirmed:
        user_input = input(f"You are going to delete {username}, do you confirm (yes/no): ").lower()
        if user_input in valid_responses:
            if user_input == 'yes':
                confirmed = True
            else:
                return False
        else:
            print("Invalid response. Answer with 'yes' ou 'no'.")
    return True

def get_password_hash(password):
    return pwd_context.hash(password)

def connect_to_db():
    name=os.getenv('name')  
    password=os.getenv('password')
    #password = get_password_hash(password) #2nd hash of the admin password used to connect to the DB
    global database_name
    global container_name
    session=database.start_a_db_session(
        DB_Username_For_Admin=name,
        DB_Password_For_Admin=password,
        DB_Name_For_Users_Tables=database_name,
        DB_Container_Name=container_name
        )
    return session

def auto_logout():
    time.sleep(30)
    os.putenv('username', '')
    os.putenv('password', '')
    typer.secho(f"You are now disconnected, if you want to keep using the CLI you need to reconnect", fg=typer.colors.RED)
    os.system('bash')
    return exit

if __name__ == "__main__":
    app()





        