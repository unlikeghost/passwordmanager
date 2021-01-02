#!/bin/bash
pip3 install virtualenv
sudo mkdir /usr/local/bin/passmanager
sudo mv *.py *.txt *md *.sh /usr/local/bin/passmanager
cd /usr/local/bin/passmanager
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x main.py
cd ..
printf 'cd pasmanager\nsource env/bin/activate\n python main.py' > password-manager.sh