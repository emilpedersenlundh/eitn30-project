import argparse
import sys
import argparse
import time
import struct
import board
import digitalio
import numpy as np

from matplotlib import use
from RF24 import RF24, RF24_PA_LOW

SPI_SPEED = 2000000 #Hz

SPI0 = {
    'MOSI':10,#dio.DigitalInOut(board.D10),
    'MISO':9,#dio.DigitalInOut(board.D9),
    'clock':11,#dio.DigitalInOut(board.D11),
    'ce':digitalio.DigitalInOut(board.D17),
    'csn':digitalio.DigitalInOut(board.D8),
    }

SPI1 = {
    'MOSI':20,#dio.DigitalInOut(board.D10),
    'MISO':19,#dio.DigitalInOut(board.D9),
    'clock':21,#dio.DigitalInOut(board.D11),
    'ce':digitalio.DigitalInOut(board.D27),
    'csn':digitalio.DigitalInOut(board.D18),
    }

radio = RF24(SPI0['ce'], SPI0['csn'], SPI_SPEED)

def transmit(address):
    print("Transmitter")

def receive(address, channel):
    

def mode(userinput: str=""):
    mode = ""
    if userinput == "TX" or userinput == "RX":
        mode = userinput
    else:
        print("No mode specified, defaulting to receiver..")
        mode = "RX"
    print("Role = {}".format(mode))
    return mode

if __name__ == "__main__":
    print("lol")
    role = mode(sys.argv[0])