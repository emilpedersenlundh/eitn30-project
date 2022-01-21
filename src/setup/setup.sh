#!/usr/bin/env bash

#Read pi number for connecting via ssh
echo "Please provide pi-nbr"
read pinbr
address="inutiuser@inuti$pinbr.lab.eit.lth.se"
repository="https://github.com/emilpedersenlundh/eitn30-project.git"

ROOT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $ROOT_PATH
cd ..
pwd

#Create temporary folder
mkdir ~/temp

##BUG: Connecting via SSH works differently than what was assumed when writing the code below.
#Transfer pub key
scp ~/.ssh/id_rsa.pub "$address:~/temp/key-temp"

#start ssh sessions
ssh $address < "LangGeNot5G"

##Authorize key
cat ~/temp/key-temp >> .ssh/authorized_keys

#Configure git
git config user.name "internetinuti"
git config user.email "lolxd@lolxd.com"

#Git repository
#Check if exists, else make directory and install
if [[ -f "~/git/" ]]
then
    echo "Git directory exists. Skipping creation."

    #Check if exists, else install
    if [[ -f "~/git/eitn30-project/" ]]
    then
        echo "Git repository exists, updating."
        cd ~/git/eitn30-project/
        git pull
    else
        echo "Git repository missing, cloning."
        cd ~/git/
        git clone $repository
    fi
else
    echo "Git directory missing. Creating and cloning repository."
    mkdir ~/git/
    cd ~/git/
    git clone $repository
fi


#fix permissions
cd ~/git/
chmod -R u+x eitn30-project/
cd ~/git/eitn30-project/

#Install radio dependencies
#C++ Library
#Check if exists, else install
if [[ -f "~/git/eitn30-project/rf24libs/RF24/" ]]
then
    echo "RF24 directory exists on system."
else

fi
#cd ~/temp
#wget http://tmrh20.github.io/RF24Installer/RPi/install.sh
#chmod u+x install.sh

sudo apt update
sudo apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essentials python3-pip
sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so

#./install.sh

#Download python libraries
python3 -m pip install --upgrade pip setuptools

#Setup virtual interface
#modprobe tun
