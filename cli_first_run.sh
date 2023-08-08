#!/bin/bash
sudo apt-get install python3-venv
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
