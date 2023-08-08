#!/bin/bash
sudo apt-get install python3-venv

sudo apt install wget
sudo wget https://dlm.mariadb.com/3216102/Connectors/c/connector-c-3.3.5/mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz
tar -xzvf mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz
cd mariadb-connector-c-3.3.5-debian-buster-amd64
sudo cp lib/* /usr/lib/
sudo cp include/* /usr/include/
sudo ldconfig
cd ..
rm -r  mariadb-connector-c-3.3.5-debian-buster-amd64
rm -r  mariadb-connector-c-3.3.5-debian-buster-amd64.tar.gz

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
