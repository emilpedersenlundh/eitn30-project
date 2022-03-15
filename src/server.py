#!/home/fideloper/.envs/eitn30-project/bin/python3

from asyncio import QueueEmpty
import os
import fcntl
import struct
import random
import subprocess
from multiprocessing import Queue

class Server:

    def __init__(self, mode: str):

        self.iface = 'longge'
        self.ip = '10.10.10.{}'.format(random.randint(2,254))
        self.mode = mode.upper
        self.tun = Interface(self.iface, self.ip, self.mode)
        print("Started server {}:{} as {}".format(self.iface, self.ip, self.mode))

    def read(self):
        """
        Read from TUN interface.
        """
        self.tun.read()

    def write(self, buffer: list[Queue]):
        """
        Writes to TUN interface. If successful returns true, else false.
        """
        #Expect buffer[i, q: Queue]
        for i in buffer:
            try:
                data = buffer[i].get(False)
                written = self.tun.write(data)
                return written
            except QueueEmpty as e:
                print('Buffer pipe {}: \n{}'.format(i, e))

    def set_ip(self, ip):
        """
        Sets IP of the Tun interface.
        """
        self.tun.set_ip(ip)
        self.ip = ip

class Interface:

    def __init__(self, iface, ip, mode):
        # Tun Attributes
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_NO_PI = 0x1000
        self.iface = iface
        self.mode = mode
        self.mtu = 1500
        self.ip = ip

        # Opens already existing TUN interface
        self.tun = open('/dev/net/tun', 'r+b', 0)
        ifr= struct.pack('16sH', bytes(iface,'utf-8'), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.tun, TUNSETIFF, ifr)
        fcntl.ioctl(self.tun, TUNSETOWNER, 1000)

        # Sets default values for TUN interface
        self.__set_interface(self.ip)

    def __delete__(self):
        self.tun.close()

    def read(self):
        packet = os.read(self.tun.fileno(), self.mtu)
        return packet

    def write(self, buffer):
        written = os.write(self.tun.fileno(), buffer)
        if written != 0:
            return True
        return False

    def set_ip(self, ip):
        """
        Sets the IP of the server and TUN interface.
        """
        cmd_remove = "ip addr del {}/24 dev {}".format(self.ip, self.iface)
        cmd_add = "ip addr add {}/24 dev {}".format(ip, self.iface)
        subprocess.check_call(cmd_remove, shell=True)
        subprocess.check_call(cmd_add, shell=True)
        self.ip = ip
        self.__routing_init()

    def __set_interface(self, ip):
        """
        Applies settings to the TUN interface.
        """
        cmd_mtu = "mtu {}".format(self.mtu)
        cmd = "ip link set {} {}".format(self.iface, cmd_mtu)
        cmd_ip = "ip addr add {}/24 dev {}".format(ip, self.iface)
        cmd_up = "ip link set {} up".format(self.iface)
        subprocess.check_call(cmd_ip, shell=True)
        subprocess.check_call(cmd, shell=True)
        subprocess.check_call(cmd_up, shell=True)
        self.ip = ip

    def __routing_init(self):
        """
        Applies routing rules depending on operating mode.
        """
        cmd_base_a = 'iptables -t nat -A POSTROUTING -o {} -j MASQUERADE'.format(self.iface)
        cmd_base_b = 'iptables -A FORWARD -i eth0 -o {} -m state --state RELATED,ESTABLISHED -j ACCEPT'.format(self.iface)
        cmd_base_c = 'iptables -A FORWARD -i {} -o eth0 -j ACCEPT'.format(self.iface)

        cmd_node = 'ip route add default via {} dev {}'.format(self.ip, self.iface)

        if self.mode == 'BASE':
            try:
                subprocess.check_call(cmd_base_a, shell=True)
                subprocess.check_call(cmd_base_b, shell=True)
                subprocess.check_call(cmd_base_c, shell=True)
            except subprocess.CalledProcessError as e:
                print(e.output)
        else:
            try:
                subprocess.check_call(cmd_node, shell=True)
            except subprocess.CalledProcessError as e:
                print(e.output)
