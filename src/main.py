#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep

# Project packages
from server import Server as server


if __name__ == "__main__":
    s = server('longge')
    s.set_ip('10.10.10.1')

    while True:
        try:
            print(s.ip)
            sleep(0.5)

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt\n")
            exit()
