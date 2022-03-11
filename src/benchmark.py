#!/home/fideloper/.envs/eitn30-project/bin/python3

from time import sleep
from multiprocessing import Process, Queue

# Project packages
from server import Server as server

def send(q):
    i = 0
    data = ['placeholder']
    while True:
        i += 1
        q.put(data)
        sleep(1/i)

def receive(q):
    q.get()

def run_test():
    queue = Queue()
    rx = Process(target=receive, args=queue)
    tx = Process(target=send, args=queue)

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

    try:
        pass
    except KeyboardInterrupt:
        print("\n Keyboard Interrupt\n")
        Process.kill()
        quit()
