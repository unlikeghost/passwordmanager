#!/bin/bash
pip3 install virtualenv
sudo mkdir /usr/local/bin/passmanager
sudo mv *.py *.txt *md *.sh /usr/local/bin/passmanager
cd /usr/local/bin/passmanager
sudo virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x consider upgrading via the '/usr/local/bin/passmanager/env/bin/python -m pip install --upgrade pip' command.main.py
sudo printf 'cd passmanager\nsource env/bin/activate\npython main.py' > pssmanager.sh
sudo mv pssmanager.sh /usr/local/bin
sudo chmod +x pssmanager.sh