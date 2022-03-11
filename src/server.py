#!/home/fideloper/.envs/eitn30-project/bin/python3

import os
import fcntl
import struct

class Server:

    def __init__(self, iface):

        self.tun = Interface(iface)

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

    def set_ip():
        pass

class Interface:

    def __init__(self, iface):
        # Tun Attributes
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_NO_PI = 0x1000
        self.mtu = 2048

        # Opens already existing TUN interface
        self.tun = open('/dev/net/tun', 'r+b', 0)
        ifr= struct.pack('16sH', bytes(iface,'utf-8'), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.tun, TUNSETIFF, ifr)
        fcntl.ioctl(self.tun, TUNSETOWNER, 1000)

    def read(self):
        packet = os.read(self.tun.fileno(), self.mtu)
        return packet

    def write(self, buffer):
        written = os.write(self.tun.fileno(), buffer)
        if written != 0:
            return True
        return False
