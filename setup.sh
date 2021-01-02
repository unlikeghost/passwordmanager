#!/bin/bash
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x main.py
printf 'source env/bin/activate\n python main.py' password-manager.sh
sudo mv ~/myscript.sh /usr/local/bin/SCRIPTNAME