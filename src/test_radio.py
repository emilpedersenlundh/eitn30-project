#!/home/fideloper/.envs/eitn30-project/bin/python3

from subprocess import PIPE
import radio, utilities
import random
from multiprocessing import Process
import time

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]


if __name__ == '__main__':

    mode_select = input("Select mode (BASE or NODE): ").upper()
    role = utilities.mode(mode_select)

    rf = radio.Radio(role)
    count = 3
    data_buffer = [[] for _ in range(6)]
    actual = [1, 2, 2, 2, 2, 3,3]

    #test_data = bytes([random.randint(0, 255) for _ in range(100)])
    test_data = b"\x81\xd9\x11\xbbv$\x85K\x05i^m\xa2\xd7\xe4\rqTk\xe8P\xbd\xe5NM$\x1e\xa2+\xdb\n\n;3\x9a\xf4H\xfb\xc9'\xbf\xd6\xa0\x1d\xb7\xb7\x91\xb7\x95\x05\x19te\x8a\x9fG\xbb\xb7\xbd\x87\x02\xf75\xd6a=\x0fkA\xc0\xf2\x12\x85\xf9\xe1\x97.oxy\xdab\x13\x0e\xe5\xff\x17\xf7\x04\x98\x0ft\xf6\x08Qjc\x02\xaf\xe0"

    try:
        expected = (test_data)
        if role == "BASE":
            actual = rf.receive(10, data_buffer)
            print("Expected = ",list(map(hex, list(expected))))
            print("Actual = ", list(map(hex, list(actual))))
            assert expected == actual
        else:
            status = False
            pipe = 1
            while not status or pipe < 6:
                status = rf.transmit(PIPE_ADDRESSES[0], test_data)
                print(pipe)
                print("status = {}".format(status))
                pipe += 1

    except KeyboardInterrupt:
        print("\n----Keyboard interrupt----\n")
        if (role == "NODE"):
            print("RX Radio Details: \n")
            rf.rx_radio.printPrettyDetails()
        if (role == "BASE"):
            print("\nTX Radio Details:\n")
            rf.tx_radio.printPrettyDetails()
