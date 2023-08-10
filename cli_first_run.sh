#!/bin/bash
sudo apt-get update
sudo apt-get install python3-venv gcc wget python3-dev libmariadb3 libmariadb-dev
sudo wget https://downloads.mariadb.com/Connectors/c/connector-c-3.3.5/mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz -O - | sudo tar -zxf - --strip-components=1 -C /usr
echo "export LD_LIBRARY_PATH=/usr/lib/mariadb" >> ~/.bashrc
source ~/.bashrc


SCRIPT_DIR="~/CLI-Admin-test"

python3 -m venv $SCRIPT_DIR/venv

source $SCRIPT_DIR/venv/bin/activate
pip install -r $SCRIPT_DIR/cli_requirements.txt 

PYTHON_EXECUTABLE="python3"

MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc

sudo bash $SCRIPT_DIR/get_mariadb_ip.sh
