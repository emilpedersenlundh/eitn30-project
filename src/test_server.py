#!/home/fideloper/.envs/eitn30-project/bin/python3

from multiprocessing import Queue

# Project modules
from server import Server as server

def write():
    pass

def read():
    pass

if __name__ == "__main__":
    s = server('base')
    q = Queue()
    l = list()
    data = bytes('helloworld','utf-8')

    q.put(data, False)
    l.append(q)
    success = s.write(l)
    print(success)
    element = l.pop()
    read = s.read()
    print(type(read))

    print("{}\n{}".format(element.get(False), read))
