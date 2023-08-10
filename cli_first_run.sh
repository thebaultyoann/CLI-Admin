#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo apt-get update
sudo apt-get install python3-venv python3-pip python3-dev gcc wget libmariadb3 libmariadb-dev
sudo wget https://downloads.mariadb.com/Connectors/c/connector-c-3.3.5/mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz -O - | sudo tar -zxf - --strip-components=1 -C /usr
sudo echo "export LD_LIBRARY_PATH=/usr/lib/mariadb" >> ~/.bashrc
source ~/.bashrc

sudo python3 -m venv venv

source $SCRIPT_DIR/venv/bin/activate

sudo pip install -r cli_requirements.txt 

PYTHON_EXECUTABLE="python3"
    
MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc

sudo bash CLI-Admin-test/get_mariadb_ip.sh
