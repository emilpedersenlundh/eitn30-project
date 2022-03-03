#!/home/fideloper/.envs/eitn30-project/bin/python3

import os
import fcntl
import struct
from multiprocessing import Process
import socket
import scapy.all as scapy
from tuntap import TunTap

INTERFACE = ''
PORT=5000

class Server:

    def __init__(self) -> None:
        # Local variables
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def open_socket(self, interface, port):
        # Check input parameters
        self.s.bind((interface, port))
        self.s.listen(1)

#TODO: Implement send and receive on socket

iface = 'LongGe'
# Create and configure a TUN interface
tun = TunTap(nic_type="Tun", nic_name="tun0")
tun.config(ip="192.168.1.10", mask="255.255.255.0",
teway="192.168.2.2")
# Read from TUN interface
#buf = tun.read(size)
# Write to TUN interface
#tun.write(buf)
# Close and destroy interface
tun.close()
