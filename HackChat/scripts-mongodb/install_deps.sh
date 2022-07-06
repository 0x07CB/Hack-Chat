#!/bin/bash
#
# For Debian (need to be tested)
#sudo apt-get update && sudo apt-get install libcurl4 openssl liblzma5 wget
#wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-4.4.4.tgz
#tar -zxvf mongodb-linux-*-4.4.4.tgz
#cd mongodb-linux-x86_64-debian10-4.4.4/
#sudo cp bin/* /usr/local/bin/
#FOLDERS BY DEFAULTS
#sudo mkdir -p /var/lib/mongo
#sudo mkdir -p /var/log/mongodb
#sudo chown $USER /var/lib/mongo     # Or substitute another user
#sudo chown $USER /var/log/mongodb   # Or substitute another user

###for service : mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork


#
# For ARCH
git clone https://aur.archlinux.org/mongodb-bin.git
cd mongodb-bin/
makepkg -si
cd ..
rm -rf mongodb-bin
