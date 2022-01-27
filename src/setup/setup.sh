#!/usr/bin/env bash

#Read pi number for connecting via ssh
echo "Please provide pi-nbr"
read pinbr
address="inutiuser@inuti$pinbr.lab.eit.lth.se"
repository="https://github.com/emilpedersenlundh/eitn30-project.git"
repofolder="eitn30-project"
password="LangGeNot5G"

ROOT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $ROOT_PATH
cd ..
pwd

##BUG: Connecting via SSH works differently than what was assumed when writing the code below. SSH has to be passed a script in order to run it.
#Transfer pub key
scp ~/.ssh/id_rsa.pub "$address:~/temp-key"

#start ssh sessions
ssh $address < $password

#Authorize key
cat ~/temp-key >> ~/.ssh/authorized_keys
rm ~/temp-key

#Configure git
git config user.name "InternetInutiPi$pinbr"
git config user.email "notan@email.com"

#Git repository installation
if [[ -f "~/git/" ]]
then
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

#Fix permissions
cd ~/git/
chmod -R u+x eitn30-project/
cd ~/git/eitn30-project/
echo "Repository permissions set."

#Install radio dependencies
##C++ Library
##Check if exists, else install
if [[ -f "~/usr/include/RF24/" ]]
then
    echo "LibRF24 exists on system. Skipping installation."
else
    # Download latest release
    curl -s https://api.github.com/repos/nRF24/RF24/releases/latest \
    | grep "browser_download_url.*deb" \
    | grep arm64 \
    | grep RPi \
    | cut -d '"' -f 4 \
    | wget -qi -
    # Install .deb
    sudo dpkg -i ~/git/eitn30-project/librf24-RPi*arm64.deb
    rm ~/git/eitn30-project/librf24-RPi*arm64.deb
    echo "LibRF24 installed."
fi

sudo apt update
sudo apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essentials
sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so

#Install Python3 setuptools globally
python3 -m pip install --upgrade pip setuptools

#Build LibRF24 Python wrapper
cd ~/git/$repofolder/
git clone https://github.com/nRF24/RF24.git
cd ~/git/$repofolder/RF24/pyRF24/
python3 setup.py build

#Install and activate python virtual environment
if [[ -f "~/.envs/$repofolder/" ]]
then
    echo "Python venv exists. Switching to environment."
    source ~/.envs/$repofolder/bin/activate
else
    if [[ -f "~/.envs/" ]]
    then
        echo "Python venv does not exist. Creating and activating."
        python3 -m venv ~/.envs/$repofolder
        source ~/.envs/$repofolder/bin/activate
    else
        echo "Python venv does not exist. Creating and activating."
        mkdir ~/.envs/
        python3 -m venv ~/.envs/$repofolder
        source ~/.envs/$repofolder/bin/activate
    fi
fi

#Install Python3 setuptools locally
python3 -m pip install --upgrade pip setuptools

#Install LibRF24 Python wrapper
cd ~/git/$repofolder/RF24/pyRF24/
python3 setup.py install

#Setup virtual interface
#modprobe tun
