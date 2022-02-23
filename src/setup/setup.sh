#!/usr/bin/env bash

#ROOT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

password="LangGeNot5G"
repository="https://github.com/emilpedersenlundh/eitn30-project.git"
repofolder=$( basename "$repository" .git)
pinbr="$(echo $HOSTNAME | tail -c 2)"
ROOT_PATH="$HOME/git/$repofolder"

#Configure git
git config --global user.name "InternetInutiPi$pinbr"
git config --global user.email "notan@email.com"

#Git repository installation
if [[ -d "$HOME/git/" ]]
then
    if [[ -d "$ROOT_PATH" ]]
    then
        echo "Git repository exists, updating."
        cd $ROOT_PATH
        git pull
    else
        echo "Git repository missing, cloning."
        cd $HOME/git/
        git clone $repository
    fi
else
    echo "Git directory missing. Creating and cloning repository."
    mkdir $HOME/git/
    cd $HOME/git/
    git clone $repository
fi

#Update repository lists
echo $password | sudo -S apt update

#SPI Setup
#TODO: Add boot config check
#TODO: Check available SPI devices
sudo usermod -a -G spi inutiuser

##Install radio dependencies
#C++ Library
#if [[ -d "/usr/include/RF24/" ]]
#then
    #TODO: Remove old installation
    #echo "LibRF24 exists on system. Skipping installation."
#else
    ## Install latest .deb release
    # cd $HOME/git/$repofolder/src/
    # echo "Installing LibRF24."
    # curl -s https://api.github.com/repos/nRF24/RF24/releases/latest \
    # | grep "browser_download_url.*deb" \
    # | grep armhf \
    # | grep SPIDEV \
    # | cut -d '"' -f 4 \
    # | wget -qi -
    # # Install .deb
    # packagename=$(ls $HOME/git/$repofolder/*armhf.deb)
    # sudo dpkg -i $packagename
    # rm $packagename
    # echo "LibRF24 installed."

    ## Install via script.
    echo ""
    echo "Installing LibRF24."
    echo ""
    git clone https://github.com/tmrh20/RF24.git ${ROOT_PATH}/RF24
    echo ""

    cd ${ROOT_PATH}/RF24
    $(./configure --driver=SPIDEV)
    cd ../..
    make -C ${ROOT_PATH}/RF24
    sudo make install -C ${ROOT_PATH}/RF24

    echo ""
    echo "*** LibRF24 installed. ***"
    echo ""
#fi

sudo apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essential libatlas-base-dev
sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so

#Install Python3 setuptools globally
python3 -m pip install --upgrade pip setuptools

#Build LibRF24 Python wrapper
echo "Building pyRF24 wrapper."
cd $ROOT_PATH/RF24/pyRF24/
python3 setup.py build
echo "Build complete."

#Install and activate python virtual environment
if [[ -d "$HOME/.envs/$repofolder/" ]]
then
    echo "Python venv exists. Switching to environment."
    source $HOME/.envs/$repofolder/bin/activate
else
    if [[ -d "$HOME/.envs/" ]]
    then
        echo "Python venv does not exist. Creating and activating."
        python3 -m venv $HOME/.envs/$repofolder
        source $HOME/.envs/$repofolder/bin/activate
    else
        echo "Python venv does not exist. Creating and activating."
        mkdir $HOME/.envs/
        python3 -m venv $HOME/.envs/$repofolder
        source $HOME/.envs/$repofolder/bin/activate
    fi
fi

#Install Python3 setuptools locally
python3 -m pip install --upgrade pip setuptools
python3 -m pip install -r $ROOT_PATH/requirements.txt

#Install LibRF24 Python wrapper
echo "Installing pyRF24 wrapper."
cd $ROOT_PATH/RF24/pyRF24/
python3 setup.py install
echo "Installation complete."

##Setup virtual interface
#sudo modprobe tun
