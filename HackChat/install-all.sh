#!/bin/bash
bash install_deps.sh
#
cp config_connect.json /etc/hackchat/core/config_connect.json
#
sudo mkdir -p /etc/hackchat/core/
sudo cp HackChat.py /etc/hackchat/core/HackChat.py
sudo chmod a+x /etc/hackchat/core/HackChat.py
sudo chmod a-w /etc/hackchat/core/HackChat.py
sudo ln -i /etc/hackchat/core/HackChat.py /usr/bin/hackchat
#
sudo cp 4push.json /etc/hackchat/core/4push.json
sudo cp 4push.txt /etc/hackchat/core/4push.txt
sudo ln -i /etc/hackchat/core/4push.json /etc/hackchat/4push.json
sudo ln -i /etc/hackchat/core/4push.txt /etc/hackchat/4push.txt
