import typer
from typing import Callable 
from functools import wraps
from typing_extensions import Annotated
import os

import authentification
import database

#resource.setrlimit(resource.RLIMIT_CORE, (0, 0))  #to activated when going to production. Stop the authenticated_user from being shown when core dump happens

app = typer.Typer()

import os

@app.command()
def login(name: str, password: Annotated[str, typer.Option(prompt=True, hide_input=True)]): 
    command = f'export name={name} && export password={password} && source ~/Documents/admin/venv/bin/activate && exec bash'
    os.system(f'gnome-terminal -- bash -ic "{command}"')


@app.command()
def open_a_session_with_db():
    name=os.getenv('name')
    password=os.getenv('password')
    session=database.start_a_db_session(name,password,"adminuserdatabase")
    user = database.get_user_name(session)
    
if __name__ == "__main__":
    app()
