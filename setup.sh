#!/bin/bash
pip3 install virtualenv
sudo mkdir /usr/local/bin/passmanager
sudo mv *.py *.txt *md *.sh /usr/local/bin/passmanager
cd /usr/local/bin/passmanager
sudo virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x main.py
sudo printf '#!/bin/bash\ncd /usr/local/bin/passmanager\nsource env/bin/activate\npython main.py' > pssmanager
sudo mv pssmanager.sh /usr/local/bin
sudo chown root: /usr/local/bin/pssmanager
sudo chmod +x /usr/local/bin/pssmanager