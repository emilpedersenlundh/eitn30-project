#!/home/fideloper/.envs/eitn30-project/bin/python3

from ctypes import c_uint16
import sys
import argparse
import time
import struct
import typing
import board
import digitalio
import numpy as np

from RF24 import RF24, RF24_PA_LOW

SPI_SPEED = 10000000 #Hz
LOCAL_ADDRESS = [] #Lägga in lokal ip

LOCAL_PACKET = {
    #Preamble
    #Address
    #Packet control field: Payload length, Packet ID, No ACK
    #Payload
    #CRC
}

#6 slots for addresses
IP_TABLE = np.array([1 for _ in range(6)])

#Data buffer for all pipes in rx (128 bytes)
DATA_BUFFER = np.array([[np.int8 for _ in range(128)] for _ in range(len(IP_TABLE))])

SPI0: c_uint16 = {
    'MOSI':10,#dio.DigitalInOut(board.D10),
    'MISO':9,#dio.DigitalInOut(board.D9),
    'clock':11,#dio.DigitalInOut(board.D11),
    'ce':17,#digitalio.DigitalInOut(board.D17),
    'csn':8#digitalio.DigitalInOut(board.D8),
    }
SPI1: c_uint16 = {
    'MOSI':20,#dio.DigitalInOut(board.D10),
    'MISO':19,#dio.DigitalInOut(board.D9),
    'clock':21,#dio.DigitalInOut(board.D11),
    'ce':27,#digitalio.DigitalInOut(board.D27),
    'csn':18#digitalio.DigitalInOut(board.D18),
    }

### Implement separate socket server which listens to the virtual interface and relays packets (also implements sending packets, i.e. the reverse)

tx_radio = RF24(SPI0['ce'], SPI0['csn'], SPI_SPEED)
rx_radio = RF24(SPI1['ce'], SPI1['csn'], SPI_SPEED)

def setup():
    # Initialize radio, if error: return runtime error
    # Set power amplifier level
    # Set CRC encoding
    # Set CRC enable/disable
    # Set address width
    # Set auto-retransmit delay
    # Set auto-retransmit limit
    # Set channel
    # Set data rate
    # Set payload size (dynamic/static)

    #print ("csn: {}, ce: {}, SPIspeed: {}".format(SPI0['csn'] , SPI0['ce'] , SPI_SPEED))
    tx_radio.begin()

## Control plane
def discover():
    # Announce self
    # Listen for responses(account for collisions)
    # Add to unauthenticated contacts array
    print("Discover")

def authenticate():
    # Authenticate node (e.g. with PKI)
    print("Authenticate")

def associate():
    # Add node to address array with lease timestamp
    # If TDMA: Add to schedule, sync clocks
    # Else apply random access scheme
    print("Associate")

def disassociate():
    # If lease != expired: Inform node of disassociation
    # Remove node from address array
    print("Disassociate")

def transmit(tx_radio, address):
    tx_radio.open_tx_pipe(address)  # set address of RX node into a TX pipe
    tx_radio.listen = False
    tx_radio.channel = 1
    count = 10

    status = []
    buffer = np.random.bytes(32)

    start = time.monotonic()
    while count:
        # use struct.pack to packetize your data
        # into a usable payload

        #buffer = struct.pack("<i", count)
        # 'i' means a single 4 byte int value.
        # '<' means little endian byte order. this may be optional
        #print("Sending: {} as struct: {}".format(count, buffer))
        result = tx_radio.send(buffer)
        if not result:
            #print("send() failed or timed out")
            #print(tx_radio.what_happened())
            status.append(False)
        else:
            #print("send() successful")
            status.append(True)
        # print timer results despite transmission success
        count -= 1
    total_time = time.monotonic() - start

    print('{} successfull transmissions, {} failures, {} bps'.format(sum(status), len(status)-sum(status), 32*8*len(status)/total_time))
    #TODO: Replace ^ 32 with size
def receive(rx_radio, timeout):
    # Make sure all 6 pipes are open
    #index: bytes
    #address: bytes
    #for index, address in enumerate(IP_TABLE):
    rx_radio.openReadingPipe(0, b"\x78" * 5)
    # Start listening'
    rx_radio.startListening()
    start = time.time()
    # Timeout condition
    while(time.time() - start < timeout):
        #Checks if there are bytes available for read
        payload_available, pipe_nbr = rx_radio.available_pipe()
        if(payload_available):
            # If has payload, read radio packet size
            payload_size = rx_radio.getDynamicPayloadSize()
            datatest = rx_radio.read(payload_size)
            DATA_BUFFER[pipe_nbr] = rx_radio.read(payload_size)
            print("Received a payload in pipe {} of size {}bytes and data {}".format(pipe_nbr, payload_size, datatest))
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
    if userinput == "BASE" or userinput == "NODE":
        mode = userinput
    else:
        print("No mode specified, defaulting to NODE..")
        mode = "NODE"
    print("Role = {}".format(mode))
    return mode

if __name__ == "__main__":

    setup()
    dest_addr = 1
    runtime = 5000
    role = mode(sys.argv[0])
    count = 3

    while count:
        if(role == "BASE"):
            start = time.time()
            while(time.time() - start < runtime):
                transmit(tx_radio, dest_addr)
        else:
            start = time.time()
            receive(rx_radio, runtime)
        count -= 1
