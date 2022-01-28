#!/usr/bin/env bash

## Dependencies:
# sshpass
if [[ $(dpkg -s sshpass | grep "install ok") != "Status: install ok installed" ]]
then
    echo "Installing sshpass (required)"
    sudo apt install sshpass
fi

## Attributes
password="LangGeNot5G"
pubkeypath="$HOME/.ssh/eitn30.pub"
pubkeyname="eitn30.pub"
authorize="cat ~/$pubkeyname >> ~/.ssh/authorized_keys; rm ~/$pubkeyname"

## Script

# Set public key path
read -p "Would you like to provide a custom public key path?[Y/n)" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Please enter pubkey path (e.g. /home/*/.ssh/*)"
    read input
    pubkeypath="$(echo -e "$input" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    pubkeypath="$(realpath $input)"
    echo
    # Set name of public key
    pubkeyname=$(basename $pubkeypath)
fi

# Dial to each machine and authorize user
echo "Dialing to machines and authorizing public key."
for i in 0{1..9} {10..20}
do
    adress="inutiuser@inuti$i.lab.eit.lth.se"
    sshpass -p $password scp -q -o StrictHostKeyChecking=no $pubkeypath $adress:~/
    sshpass -p $password ssh -t -q -o StrictHostKeyChecking=no $adress $authorize
done

echo
echo "Script finished."
echo "If you're using Windows+WSL make sure both SSH configs and keys are correct"
echo "Good hunting."
echo
