#!/usr/bin/env bash

#Read pi number for connecting via ssh
echo "Please provide pi-nbr"
read pinbr
address="inutiuser@inuti$pinbr.lab.eit.lth.se"
ROOT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $ROOT_PATH
cd ..
pwd

#Create temporary folder
mkdir ~/temp

#Transfer pub key
scp ~/.ssh/id_rsa.pub "$address:~/temp/key-temp"

#start ssh sessions
ssh $address < "LangGeNot5G"

##Authorize key
cat ~/temp/key-temp >> .ssh/authorized_keys

#Configure git
git config user.name "internetinuti"
git config user.email "lolxd@lolxd.com"

#clone repo
mkdir ~/git
cd ~/git
git clone https://github.com/emilpedersenlundh/eitn30-project.git

#fix permissions
chmod -R u+x eitn30-project/

cd ~git/eitn30-project/

#Install radio dependencies
#C++ Library
#Check if exists, else install
if [[ -f "~/" ]]
then
    echo "This file exists on your filesystem."
else

fi
cd ~/temp
wget http://tmrh20.github.io/RF24Installer/RPi/install.sh
chmod u+x install.sh
./install.sh


#Python dependencies
sudo apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio

sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so

#Download python libraries
python3 -m pip install --upgrade pip setuptools

#Setup virtual interface
modprobe tun
