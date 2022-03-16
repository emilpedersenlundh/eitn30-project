#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep

# Project packages
from server import Server as server
import radio, utilities

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]

def run_node(radio):
    pass

def run_base(radio, server data_buffer):

    received = False
    timeout = 10

    while not received:
        received = radio.receive(timeout, data_buffer)
    
    



if __name__ == "__main__":

    data_buffer = [[] for _ in range(6)]

    role = utilities.mode(input("Select mode (BASE or NODE): ").upper())

    # Start services
    s = server(role)
    r = radio.Radio(role)

    try:
        print("Currently set IP: {}".format(s.ip), end='\r')

        if(role == "BASE"):
            run_base(r, data_buffer)
        else:
            run_node(r)

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt\n")
        exit()
