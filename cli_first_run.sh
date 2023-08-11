#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo python3 -m venv venv

source $SCRIPT_DIR/venv/bin/activate 

sudo $SCRIPT_DIR/venv/bin/python -m pip install -r cli_requirements.txt 

PYTHON_EXECUTABLE="python3"
    
MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc


