#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep

# Project packages
from server import Server as server


if __name__ == "__main__":
    mode = 'base'
    s = server(mode)
    s.set_ip('10.10.10.1')

    while True:
        try:
            print("Currently set IP: {}".format(s.ip), end='\r')
            sleep(1)

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt\n")
            exit()
