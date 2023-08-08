#!/bin/bash
sudo apt-get update
sudo apt-get install python3-venv gcc wget
sudo wget https://downloads.mariadb.com/Connectors/c/connector-c-3.3.5/mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz -O - | sudo tar -zxf - --strip-components=1 -C /usr
echo "export LD_LIBRARY_PATH=/usr/lib/mariadb" >> ~/.bashrc
source ~/.bashrc

python3 -m venv venv

source venv/bin/activate
pip install -r cli_requirements.txt

PYTHON_EXECUTABLE="python3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MAIN_SCRIPT="$SCRIPT_DIR/cli.py"

alias_command="alias cli=\"$PYTHON_EXECUTABLE $MAIN_SCRIPT\""

echo "source $SCRIPT_DIR/venv/bin/activate" >> ~/.bashrc

echo "$alias_command" >> ~/.bashrc

source ~/.bashrc
