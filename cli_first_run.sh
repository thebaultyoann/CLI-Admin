#!/bin/bash
sudo apt-get install python3-venv
sudo apt-get install gcc wget 

python3 -m venv venv

VENV_ACTIVATE="venv/bin/activate"

source $VENV_ACTIVATE

sudo wget https://dlm.mariadb.com/2678579/Connectors/c/connector-c-3.3.3/mariadb-connector-c-3.3.3-debian-buster-amd64.tar.gz -O - | tar -zxf - --strip-components=1 -C /usr      
pip install -r cli_requirements.txt

PYTHON_EXECUTABLE="python3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc
