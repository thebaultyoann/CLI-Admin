#!/bin/bash
sudo apt-get install python3-venv

sudo apt install wget
wget https://r.mariadb.com/downloads/mariadb_repo_setup
echo "3a562a8861fc6362229314772c33c289d9096bafb0865ba4ea108847b78768d2  mariadb_repo_setup" \
    | sha256sum -c -
chmod +x mariadb_repo_setup
sudo ./mariadb_repo_setup \
   --mariadb-server-version="mariadb-10.6"

sudo apt install libmariadb3 libmariadb-dev

python3 -m venv venv

VENV_ACTIVATE="venv/bin/activate"

source $VENV_ACTIVATE
pip install -r cli_requirements.txt

PYTHON_EXECUTABLE="python3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc
