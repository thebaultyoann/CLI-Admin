import typer
from typing import Callable 
from functools import wraps
from typing_extensions import Annotated
import os
import mariadb
import sqlalchemy.exc

import database

app = typer.Typer()
user_app = typer.Typer()
app.add_typer(user_app, name="user")

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if user_authentificated():
            return function(*args, **kwargs)
        else:
            return typer.secho(f"Wrong credentials", fg=typer.colors.RED)
    return wrapper

def user_authentificated():
    name=os.getenv('name')  
    password=os.getenv('password')
    if name==None or password==None:
        typer.secho(f"You need to login", fg=typer.colors.RED)
        return False
    try: 
        print("test")
        database.start_a_db_session(
            DB_Username_For_Admin=name,
            DB_Password_For_Admin=password,
            DB_Name_For_Admin_User="astrolabium",
            DB_Container_Name="172.18.0.2"
            )
    except (mariadb.OperationalError, sqlalchemy.exc.OperationalError) as e:   
        print("test2")    
        return False
    except:
        return False
    return True

@app.command("login")
def login(
    name: str, 
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)]
    ) -> None: 
    os.putenv('name',f'{name}')
    os.putenv('password',f'{password}')
    os.system('bash')

@user_app.command("list")
@login_required
def user() -> None:
    session = connect_to_db()
    user_list(session=session)

@user_app.command('add')
def user_add_command(
    username:str, 
    password: Annotated[str, typer.Option(prompt="The client password", hide_input=True)], 
    disabled: Annotated[bool, typer.Argument()]=False
    ) -> None:
    session = connect_to_db()
    user_add(session=session, username=username, password=password, disabled=disabled)
        
@user_app.command("get")
def user_get_command(username:str) -> None:
    session = connect_to_db()
    user_get(session=session, username=username)

@user_app.command("delete")
def user_delete_command(username:str) -> None:
    session = connect_to_db()
    user_delete(session=session, username=username)

@user_app.command('update')
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
        ]=None
    ) -> None:
    session = connect_to_db()
    user_update(session=session, username=username, newUsername = newUsername, password=newPassword, disabled=deactivate)
        
@user_app.command('activate')
def user_activate_command(username:str) -> None:
    session = connect_to_db()
    user_activate(session=session, username=username)


@user_app.command('deactivate')
def user_deactivate_command(username:str) -> None:
    session = connect_to_db()
    user_deactivate(session=session, username=username)

def connect_to_db():
    name=os.getenv('name')  
    password=os.getenv('password')
    session=database.start_a_db_session(
        DB_Username_For_Admin=name,
        DB_Password_For_Admin=password,
        DB_Name_For_Admin_User="astrolabium",
        DB_Container_Name="172.18.0.2"
        )
    return session

def user_update(session, username:str, newUsername:str, password:str,  disabled:bool):
    code = database.update_user(session=session, username=username, newUsername=newUsername, password=password, disabled=disabled)
    if "1" in code :
        typer.secho(f"User {username} disabled state is now {disabled}", fg=typer.colors.GREEN)
    if "2" in code : 
        typer.secho(f"User {username} password has been changed", fg=typer.colors.GREEN)
    if "3" in code :  
        typer.secho(f"User {username} is now {newUsername}", fg=typer.colors.GREEN)
    if (not "1" in code) and (not "2" in code) and (not "3" in code) :
        typer.secho(f"Unsuccesfull modficiation of the user {username}", fg=typer.colors.RED)

def user_activate(session, username:str):
    if database.activate_user(session=session, username=username):
        return typer.secho(f"User {username} was activated")
    return typer.secho(f"Unsuccesfull activation of the user {username}", fg=typer.colors.RED)

def user_deactivate(session, username:str):
    if database.deactivate_user(session=session, username=username):
        return typer.secho(f"User {username} was deactivated")
    return typer.secho(f"Unsuccesfull deactivation of the user {username}", fg=typer.colors.RED)

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
    user = database.delete_user(session=session, username=username)
    if user:
        typer.secho(f"User {user.username} have been delete", fg=typer.color.GREEN)
    else: 
        typer.secho("This user doesn't exist", fg=typer.colors.RED)
    
if __name__ == "__main__":
    app()
