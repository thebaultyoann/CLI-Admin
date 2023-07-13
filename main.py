import typer
from typing import Callable 
from functools import wraps
from typing_extensions import Annotated
import os

import database

#resource.setrlimit(resource.RLIMIT_CORE, (0, 0))  #to activated when going to production. Stop the authenticated_user from being shown when core dump happens

app = typer.Typer()

import os

@app.command()
def login(name: str, password: Annotated[str, typer.Option(prompt=True, hide_input=True)]): 
    os.putenv('name',f'{name}')
    os.putenv('password',f'{password}')
    os.system('bash')

@app.command()
def get_user_name():
    name=os.getenv('name')  
    password=os.getenv('password')
    session=database.start_a_db_session(name,password,"astrolabium")
    user = database.get_user_name(session)
    print(user.username)
    return
    
if __name__ == "__main__":
    app()
