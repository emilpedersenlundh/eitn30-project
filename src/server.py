#!/home/fideloper/.envs/eitn30-project/bin/python3

from ast import Not
import os
import fcntl
import struct
import typing
from multiprocessing import Process, Queue
import scapy.all as scapy
from tuntap import TunTap

class Server:

    def __init__(self, ip):
        # Local variables
        self.tun = Interface(nic_type='tun', nic_name='longge', ip_address=ip, mask='255.255.255.0', gateway='10.10.10.1')

    def read(self):
        self.tun.read()

    def write(self, buffer):
        for i in buffer:
            try:
                data = buffer[i].pop(0)
                if data != None:
                    self.tun.write(data)
            except Exception as e:
                print(e)

class Interface:

    def __init__(self, nic_type, nic_name, ip_address, mask, gateway):
        self.tun = TunTap(nic_type, nic_name)
        self.tun.ip = ip_address
        self.tun.mask = mask
        self.tun.gateway = gateway
        self.tun.mtu = 1500

    def __del__(self):
        self.tun.close()

    def read(self):
        self.tun.read(self.tun.mtu)

    def write(self, buffer):
        self.tun.write(buffer)
