#!/home/fideloper/.envs/eitn30-project/bin/python3

from multiprocessing import Process
import socket

INTERFACE = ''
PORT=5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((INTERFACE,PORT))
    s.listen(1)

#TODO: Implement send and receive on socket
