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
LOCAL_ADDRESS = [] #Lägga in lokal ip

LOCAL_PACKET = {
    #Preamble
    #Address
    #Packet control field: Payload length, Packet ID, No ACK
    #Payload
    #CRC
}

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
    'ce':dio.DigitalInOut(board.D27),
    'csn':dio.DigitalInOut(board.D18),
    }

tx_radio = RF24(SPI0['ce'], SPI0['csn'], SPI_SPEED)
rx_radio = RF24(SPI1['ce'], SPI1['csn'], SPI_SPEED)


def transmit(address):
    tx_radio.stopListening()
    print("Transmitter")

def receive(address, channel):
    # Make sure all 6 pipes are open
    # Start listening
    # Timeout condition
    # If has payload, read radio packet size
    # Save payload to a buffer for each data pipe
    print("Receiver")

def construct_packet(dest, data):
    header = {
        'version':4, #4bits
        'IHL':0, #4bits

        'DSCP':0, #6bits
        'ECN':0, #2bits

        'TotLen':0, #2bytes

        'Identification':0, #2bytes

        'Flags':0, #3bits
        'Fragment Offset':0, #13bits

        'TTL':0, #8bits

        'Protocol':0, #8bits

        'Source':0, #4bytes

        'Dest':0, #4bytes
    }

    header['Source'] = LOCAL_ADDRESS
    header['Dest'] = dest

    header_bytes = [
        (header['version'] << 4) + header['IHL'],
        (header['DSCP'] << 2) + header['ECN'],
        ((header['TotLen'] >> 8) & 0xFF),
        (header['TotLen'] & 0xFF),
        ((header['Identification'] >> 8) & 0xFF),
        (header['Identification'] & 0xFF),
        (header['Flags'] << 5) + (header['Fragment Offset'] >> (8)),
        (header['Fragment Offset'] & 0xFF),
        header['TIL'],
        header['Protocol'],
        0x00, #Checksum 2bytes
        0x00,
        (header['Source'] >> 24) & 0xFF,
        (header['Source'] >> 16) & 0xFF,
        (header['Source'] >> 8) & 0xFF,
        header['Source'] & 0xFF,
        (header['Dest'] >> 24) & 0xFF,
        (header['Dest'] >> 16) & 0xFF,
        (header['Dest'] >> 8) & 0xFF,
        header['Dest'] & 0xFF,
    ]

    sum = 0
    #compute checksum

    source_ip = LOCAL_ADDRESS
    dest_ip = dest
    data = data




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
