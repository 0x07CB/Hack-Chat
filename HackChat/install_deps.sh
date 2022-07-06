#!/bin/bash
#ARCHLINUX
sudo pacman -Syu
sudo pacman -S python3 python-pip netcat rsync net-tools gunicorn
#
git clone https://github.com/boppreh/keyboard.git
cd keyboard
sudo python3 setup.py build
sudo python3 setup.py install
cd ..
sudo rm -rf keyboard
#
git clone https://aur.archlinux.org/botsay.git
cd botsay/
makepkg -si
cd ..
rm -rf botsay
#
python3 -m pip install flask flask-wtf 
#
cd API-Server
bash install.sh
cd ..
#
cd scripts-mongodb
bash install_deps.sh
cd ..