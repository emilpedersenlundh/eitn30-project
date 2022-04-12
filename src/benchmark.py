#!/home/fideloper/.envs/eitn30-project/bin/python3

import os
import sys
from time import sleep, time
from multiprocessing import Process, Queue
import numpy as np
import pandas as pd

# Project packages
from radio import Radio as radio
from server import Server as server
import utilities as util

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6",
]

latency: list[int] = []
outcome: list[bool] = []
queue_size: list[int] = []


def add(queue):
    """Adds elements to a provided queue."""
    measurement_count: int = 100
    data = np.random.bytes(30)

    for i in range(measurement_count):
        queue.put(data)


def transmit(queue):
    """Transmits elements from the provided queue via radio."""
    r = radio("NODE")

    if not queue.empty():
        outcome.append(r.transmit(PIPE_ADDRESSES[1], queue.get()))


def run_test(queue):

    rx = Process(target=transmit, args=queue)
    tx = Process(target=add, args=queue)

    rx.start()
    sleep(1)
    tx.start()

    rx.join()
    tx.join()


if __name__ == "__main__":

    queue = Queue()
    run_test(queue)

    try:
        pass
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt\n")
