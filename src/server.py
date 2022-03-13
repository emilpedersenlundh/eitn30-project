#!/home/fideloper/.envs/eitn30-project/bin/python3

import os
import fcntl
import struct
import random
import subprocess

class Server:

    def __init__(self, mode: str):

        self.iface = 'longge'
        self.ip = '10.10.10.{}'.format(random.randint(2,254))
        self.mode = mode.upper
        self.tun = Interface(self.iface, self.ip, self.mode)
        print("Started server {}:{} as {}".format(self.iface, self.ip, self.mode))

    def read(self):
        self.tun.read()

    def write(self, buffer):
        """
        Writes to Tun interface. If successful returns true, else false.
        """
        for i in buffer:
            try:
                data = buffer[i].pop(0)
                if data != None:
                    written = self.tun.write(data)
                return written
            except Exception as e:
                print(e)

    def set_ip(self, ip):
        """
        Sets IP of the Tun interface. If successful returns true, else false.
        """
        self.ip = ip
        self.tun.set_interface(ip)
        #if str(subprocess.check_call(check, shell=True)) != ip:
        #    return False
        #return True

class Interface:

    def __init__(self, iface, ip, mode):
        # Tun Attributes
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_NO_PI = 0x1000
        self.iface = iface
        self.mtu = 1500

        # Opens already existing TUN interface
        self.tun = open('/dev/net/tun', 'r+b', 0)
        ifr= struct.pack('16sH', bytes(iface,'utf-8'), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.tun, TUNSETIFF, ifr)
        fcntl.ioctl(self.tun, TUNSETOWNER, 1000)

        # Sets default values for TUN interface
        self.set_interface(ip)

    def read(self):
        packet = os.read(self.tun.fileno(), self.mtu)
        return packet

    def write(self, buffer):
        written = os.write(self.tun.fileno(), buffer)
        if written != 0:
            return True
        return False

    def set_interface(self, ip):
        """
        Applies settings to the TUN interface.
        """
        cmd_netmask = 'netmask 255.255.255.0'
        cmd_broadcast = 'broadcast 10.10.10.255'
        cmd_mtu = "mtu {}".format(self.mtu)
        cmd = "ifconfig {} {} {} {} {}".format(self.iface, ip, cmd_netmask, cmd_broadcast, cmd_mtu)
        subprocess.check_call(cmd, shell=True)
    def __routing_init(self):
        #TODO: Apply routing rules. Depend on parameter 'mode'.
        pass
