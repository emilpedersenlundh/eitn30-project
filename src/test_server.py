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
    data = 'helloworld' #bytes('helloworld','utf-8')

    q.put(data, False)
    l.append(q)

    s.write(l)
    read = s.read()

    print(l, read)
