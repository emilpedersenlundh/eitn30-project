import argparse
import sys
import argparse
import time
import struct

from matplotlib import use
from RF24 import RF24, RF24_PA_LOW

pin = 0

radio = RF24(pin, 0)

def transmitter():
    print("Transmitter")

def receiver():
    print("Receiver")

def role(userinput: str=""):
    role = ""
    if userinput == "TX" or userinput == "RX":
        role = userinput
        #Fixa radion också
    else:
        print("No mode specified, defaulting to receiver..")
        role = "RX"
    print("Role = {}".format(role))
    return role

if __name__ == "__main__":
    print("lol")
    role = role(sys.argv[0])