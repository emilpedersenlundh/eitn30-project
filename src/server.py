#!/home/fideloper/.envs/eitn30-project/bin/python3

import os
import fcntl
import struct
from multiprocessing import Process
import socket
import scapy.all as scapy
from tuntap import TunTap

class Server:

    def __init__(self) -> None:
        # Local variables
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def open_socket(self, interface, port):
        # Check input parameters
        self.s.bind((interface, port))
        self.s.listen(1)

    def __create_tun(self, ip_address):
        # Create and configure a TUN interface
        tun = TunTap(nic_type="Tun", nic_name="longge")
        tun.config(ip=ip_address, mask="255.255.255.0", gateway="10.10.10.1")
        # Read from TUN interface
        #buf = tun.read(size)
        # Write to TUN interface
        #tun.write(buf)
        # Close and destroy interface
        tun.close()
