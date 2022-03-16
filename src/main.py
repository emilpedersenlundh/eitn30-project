#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep

# Project packages
from server import Server as server
from radio import Radio as radio
import utilities as util

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]

def run_node(radio: radio, server: server, data_buffer):
    transmitted: bool = False
    received: bool = False

    data = server.read()
    while data is None:
        data = server.read()

    transmitted = radio.transmit(PIPE_ADDRESSES[0], data)
    while not transmitted:
        transmitted = radio.transmit(PIPE_ADDRESSES[0], data)

    received = radio.receive(10, data_buffer)
    if received: server.write(data_buffer)

def run_base(radio: radio, server: server, data_buffer):

    received = False
    timeout = 10

    while not received:
        received = radio.receive(timeout, data_buffer)
    return server.write(data_buffer)

if __name__ == "__main__":

    data_buffer = [[] for _ in range(6)]

    role = util.mode(input("Select mode (BASE or NODE): ").upper())

    # Start services
    s = server(role)
    r = radio(role)
    try:
        print("Currently set IP: {}".format(s.ip), end='\r')

        while True:
            if(role == "BASE"):
                run_base(r, s, data_buffer)
            else:
                run_node(r)

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt\n")
        exit()
