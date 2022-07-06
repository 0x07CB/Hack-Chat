#!/bin/bash
#install the launch script of API com
sudo mkdir -p /etc/hackchat 
sudo cp run-server.sh /etc/hackchat/run-server.sh
sudo ln -i /etc/hackchat/run-server.sh /usr/bin/hackchat-com-api.sh

#install API
sudo cp API.py /etc/hackchat/API.py
sudo chmod a+x /etc/hackchat/API.py
sudo chmod a-w /etc/hackchat/API.py

#installation of the api com service
sudo cp hackchat.api-com-1.service /etc/systemd/system/hackchat.api-com-1.service
