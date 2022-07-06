#!/bin/bash
#Create an blank image
botsay -c "Create an virtual disk for database..."
sudo dd if=/dev/zero of=vdisk-1.img bs=512M count=20 status=progress iflag=fullblock
#Install deps
#apt install -y xfsprogs #For Debian
sudo pacman -S xfsprogs
#format disk
sudo mkfs.xfs vdisk-1.img
#Mount the image on /vmnt
sudo mkdir -p /vmnt
sudo mount vdisk-1.img /vmnt
botsay -c "Done."