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
## Script

#Progress bar function
progress() {
    local w=80 p=$1;  shift
    # create a string of spaces, then change them to dots
    printf -v dots "%*s" "$(( $p*$w/200 ))" ""; dots=${dots// /.};
    # print those dots on a fixed-width space plus the percentage etc.
    printf "\r\e[K|%-*s| %3d %% %s" "$w" "$dots" "$p" "$*";
}

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
authorize="cat ~/$pubkeyname >> ~/.ssh/authorized_keys; rm ~/$pubkeyname"

# Dial to each machine and authorize user
echo "Dialing to machines and authorizing public key."
for i in 0{1..9} {10..20}; do
    progress "$(($((10#$i))*5))"
    adress="inutiuser@inuti$i.lab.eit.lth.se"
    echo $adress
    end=$((SECONDS+6))
    while [ $SECONDS -lt $end ]; do
    sshpass -p $password scp -q -o StrictHostKeyChecking=no $pubkeypath $adress:~/
    sshpass -p $password ssh -t -q -o StrictHostKeyChecking=no $adress $authorize
    break
    done
done; echo

echo
echo "Script finished."
echo "If you're using Windows+WSL make sure both SSH configs and keys are correct"
echo "Good hunting."
echo
