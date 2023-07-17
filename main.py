import typer
from typing import Callable 
from functools import wraps
from typing_extensions import Annotated
import os
import resource

import database

#resource.setrlimit(resource.RLIMIT_CORE, (0, 0))  #to activated when going to production. Stop the authenticated_user from being shown when core dump happens

app = typer.Typer()
user_app = typer.Typer()
app.add_typer(user_app, name="user")

@app.command("login")
def login(name: str, password: Annotated[str, typer.Option(prompt=True, hide_input=True)]): 
    os.putenv('name',f'{name}')
    os.putenv('password',f'{password}')
    os.system('bash')

@user_app.command("list")
def user() -> None:
    session = connect_to_db()
    user_list(session=session)

@user_app.command('add')
def get_user(username:str, disabled:Annotated[bool, typer.Argument()]=False, password : Annotated[str, typer.Option(prompt=True, hide_input=True)]) -> None:
    session = connect_to_db()
    user_add(session=session, username=username, password=password, disabled=disabled)
    return print(user.username)
        
@user_app.command("get")
def user(username:str) -> None:
    session = connect_to_db()
    user_get(session=session, username=username)

@user_app.command("delete")
def user(username:str) -> None:
    session = connect_to_db()
    user_delete(session=session, username=username)


def connect_to_db():
    name=os.getenv('name')  
    password=os.getenv('password')
    session=database.start_a_db_session(
        DB_Username_For_Admin=name,
        DB_Password_For_Admin=password,
        DB_Name_For_Admin_User="astrolabium",
        DB_Container_Name="172.19.0.2"
        )
    return session


def user_list(session):
    users = database.get_all_users(session)
    if len(users) == 0:
        typer.secho(
            "There are no users in the database yet", fg=typer.colors.RED
        )
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
        return typer.secho(f"User {username} was added to the database and his disabled state is {distabled}")
    return typer.secho(f"Unsuccesfull add of the user {username}")

def user_get(session, username:str):
    user = database.get_a_single_user(session=session, username=username)
    if len(user) == 0:
        typer.secho(
            "This user doesn't exist", fg=typer.colors.RED
        )
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
        typer.secho(f"User {user.username} have been delete")
    else: 
        typer.secho(f"This user doesn't exist")

if __name__ == "__main__":
    app()
