#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep

# Project packages
from server import Server as server


if __name__ == "__main__":
    mode = 'base'
    s = server(mode)
    s.set_ip('10.10.10.1')
    i = 0

    while True:
        try:
            i += 1
            if i == 255: i = 1
            s.set_ip('10.10.10.{}'.format(i))
            print("Currently set IP: {}".format(s.ip), end='\r')
            sleep(5)

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt\n")
            exit()
