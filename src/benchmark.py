#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep
import time
from multiprocessing import Process, Queue
import numpy as np
import matplotlib.pyplot as plt

# Project packages
import radio, utilities
from server import Server as server

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]

time_axis = np.flip(np.linspace(0, 1, 0.001), axis=1)
queue_len_axis = []
latency = []

def add(q):

    global time_axis

    data = bytes("HEJHEJHEJ", "UTF-8")
    count = 0

    while count < len(time_axis):
        q.put(data)
        queue_len_axis.append(q.qsize())
        sleep(time_axis[count])
        count += 1

def receive(q):

    mode_select = input("Select mode (BASE or NODE): ").upper()
    role = utilities.mode(mode_select)
    r = radio.Radio(role)
    kill = 0

    while True and kill < 10000000:
        if not q.empty():
            start = time.time()
            r.transmit(PIPE_ADDRESSES[1], q.get())
            latency.append(time.time() - start)
        kill += 1


def run_test(queue):
    
    rx = Process(target=receive, args=queue)
    tx = Process(target=add, args=queue)

    rx.start()
    sleep(1)
    tx.start()

    rx.join()
    tx.join()

if __name__ == '__main__':

    #Pseudo
    """
    Increase send rate while keeping receive rate consistent. Measure amount of elements in queue compared to send rate (amount>0 <-> rho>1).
    """
    queue = Queue()
    run_test(queue)

    plt.plot(time_axis, queue_len_axis)
    plt.xlabel = "time"
    plt.ylabel = "queue_len"
    plt.show()
    

    try:
        pass
    except KeyboardInterrupt:
        print("\n Keyboard Interrupt\n")
        Process.kill()
        quit()
