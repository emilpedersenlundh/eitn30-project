#!/usr/bin/env bash

#Read pi number for connecting via ssh
echo "Please provide pi-nbr"
read pinbr
address="inutiuser@inuti$pinbr"

#Transfer pub key
scp ~/.ssh/id_rsa.pub "$address:~/temp"

#start ssh sessions
ssh $address < "LangGeNot5G"

##Authorize key
cat ~/temp >> .ssh/authorized_keys

#Configurate git
git config user.name $pinbr
git config user.email "lolxd@lolxd.com"

#clone repo
mkdir ~/git
cd ~/git
git clone https://github.com/emilpedersenlundh/eitn30-project.git

#fix permissions
chmod -R u+x eitn30-project/

#Download python libraries
python3 -m pip install --upgrade pip setuptools

#Setup virtual interface
modprobe tun
