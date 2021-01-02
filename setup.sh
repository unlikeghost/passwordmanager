#!/bin/bash
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x main.py
printf '[Desktop Entry]\nVersion=1.0\nName=Password-Manager\nExec=./main.py\nIcon=src/img/icon.png\nType=Aplication' > password-manager.desktop
printf 'source env/bin/activate\n python main.py' password-manager.sh