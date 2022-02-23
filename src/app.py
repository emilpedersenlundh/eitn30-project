#!/home/fideloper/.envs/eitn30-project/bin/python3

import array
from ctypes import c_byte, c_uint, c_uint16, c_uint32, c_uint8
import string
import sys
import argparse
import time
import struct
import typing
import numpy as np
import RPi.GPIO as GPIO

from RF24 import RF24, RF24_PA_LOW

SPI_SPEED: c_uint32 = 10000000 #Hz
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
DATA_BUFFER = np.array([[] for _ in range(len(IP_TABLE))])

SPI0 = {
    'SPI':0,
    'MOSI':10,#dio.DigitalInOut(board.D10),
    'MISO':9,#dio.DigitalInOut(board.D9),
    'clock':11,#dio.DigitalInOut(board.D11),
    'ce':17,#digitalio.DigitalInOut(board.D17),
    'csn':8#digitalio.DigitalInOut(board.D8),
    }
SPI1 = {
    'SPI':10,
    'MOSI':20,#dio.DigitalInOut(board.D10),
    'MISO':19,#dio.DigitalInOut(board.D9),
    'clock':21,#dio.DigitalInOut(board.D11),
    'ce':27,#digitalio.DigitalInOut(board.D27),
    'csn':18#digitalio.DigitalInOut(board.D18),
    }

PIPE_ADDRESSES = [
    b"\x78" * 5,
    b"\xF1\xB6\xB5\xB4\xB3",
    b"\xCD\xB6\xB5\xB4\xB3",
    b"\xA3\xB6\xB5\xB4\xB3",
    b"\x0F\xB6\xB5\xB4\xB3",
    b"\x05\xB6\xB5\xB4\xB3"
]

""" GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPI0['csn'], GPIO.OUT)
GPIO.setup(SPI0['ce'], GPIO.OUT)
GPIO.setup(SPI0['MOSI'], GPIO.OUT)
GPIO.setup(SPI0['MISO'], GPIO.IN)
GPIO.setup(SPI1['csn'], GPIO.OUT)
GPIO.setup(SPI1['ce'], GPIO.OUT)
GPIO.setup(SPI1['MOSI'], GPIO.OUT)
GPIO.setup(SPI1['MISO'], GPIO.IN)
GPIO.setup(SPI1['clock'], GPIO.OUT) """



### Implement separate socket server which listens to the virtual interface and relays packets (also implements sending packets, i.e. the reverse)

#tx_radio = RF24(SPI0['SPI'],SPI0['csn'], SPI0['ce'], SPI_SPEED)
#rx_radio = RF24(SPI1['SPI'],SPI1['csn'], SPI1['ce'], SPI_SPEED)
#tx_radio = RF24(SPI0['ce'], SPI0['csn'], SPI_SPEED)
#rx_radio = RF24(SPI1['ce'], SPI1['csn'], SPI_SPEED)
#tx_radio = RF24(17, 0)
#rx_radio = RF24(27, 10)

tx_radio = RF24(SPI0['ce'], SPI0['SPI'])
rx_radio = RF24(SPI1['ce'], SPI1['SPI'])

def setup():

    # Initialize radio, if error: return runtime error
    rx_radio.begin()
    tx_radio.begin()

    # Set power amplifier level
    rx_radio.setPALevel(RF24_PA_LOW)
    tx_radio.setPALevel(RF24_PA_LOW)

    # Set payload size (dynamic/static)
    rx_radio.enableDynamicPayloads
    tx_radio.enableDynamicPayloads

    # Set CRC encoding

    # Set CRC enable/disable

    # Set address width
    width: c_uint8 = 5
    rx_radio.setAddressWidth(width)
    tx_radio.setAddressWidth(width)

    # Set auto-retransmit delay

    # Set auto-retransmit limit

    # Set auto-ACK (This might fix available pipe always returning true, could also be broken module)
    #rx_radio.setAutoAck(False)

    # Set channel
    rx_radio.setChannel(108)
    tx_radio.setChannel(108)

    # Set data rate

    # Open pipes
    for pipe, address in enumerate(PIPE_ADDRESSES):
        rx_radio.openReadingPipe(pipe, address)
        #tx_radio.openWritingPipe(pipe, address)

    # Flush buffers
    rx_radio.flush_rx()
    rx_radio.flush_tx()
    tx_radio.flush_rx()
    tx_radio.flush_tx()

    #print ("csn: {}, ce: {}, SPIspeed: {}".format(SPI1['csn'] , SPI1['ce'] , SPI_SPEED))
    #rx_radio.begin(SPI1['ce'], SPI1['ce'], SPI1['csn'])

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
    # Set staggered retransmit delay if enabled
    print("Associate")

def disassociate():
    # If lease != expired: Inform node of disassociation
    # Remove node from address array
    print("Disassociate")

def transmit(tx_radio, address):

    count = 10
    size = 32
    status = []
    buffer = np.random.bytes(size)

    start = time.monotonic()
    while count:
        # use struct.pack to packetize your data
        # into a usable payload

        buffer = struct.pack("<", count)
        # 'i' means a single 4 byte int value.
        # '<' means little endian byte order. this may be optional
        print("Sending: {} as struct: {}".format(count, buffer))
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

    print('{} successfull transmissions, {} failures, {} bps'.format(sum(status), len(status)-sum(status), size*8*len(status)/total_time))

def receive(rx_radio, timeout):

    print('Rx NRF24L01+ started w/ power {}, SPI freq: {}hz'.format(rx_radio.getPALevel(), SPI_SPEED))

    # Start listening
    rx_radio.startListening()
    start = time.time()

    # Timeout condition
    while(time.time() - start < timeout):

        #Checks if there are bytes available for read
        payload_available, pipe_nbr = rx_radio.available_pipe()
        print("Payload available = {} \nPipe number = {}".format(payload_available, pipe_nbr))

        if(payload_available):

            # If has payload, read radio packet size
            payload_size = rx_radio.getDynamicPayloadSize()
            payload = struct.unpack(rx_radio.read("<", payload_size))
            print("Payload size = {} \nPayload = {}".format(payload_size, np.ravel(np.array(payload))))

            # Insert payload into data buffer
            DATA_BUFFER[pipe_nbr] = np.array([payload])
            print("Received a payload in pipe {} of size {}bytes and data {}".format(pipe_nbr, payload_size, np.ravel(DATA_BUFFER[pipe_nbr])))

            # Flush rx buffer
            #rx_radio.flush_rx()

            # Reset the timeout timer
            start = time.time()

    # Timeout
    print("Timeout")
    rx_radio.stopListening()

def construct_packet(dest_address: string, data: list, broadcast: bool = False):

    # Invalid addresses (unless broadcast is set)
    if(not broadcast):
        not_allowed = ("0.0.0.0.0", "255.255.255.255")

    header = {
        'version':0b0100, #4bits
        'IHL':0b0101, #4bits

        'DSCP':0b000000, #6bits
        'ECN':0b00, #2bits

        'TotLen':0x003c, #2bytes

        'Identification':0x1c46, #2bytes

        'Flags':0b010, #3bits
        'Fragment Offset':0b0000000000000, #13bits

        'TTL':0x40, #8bits

        'Protocol':0x06, #8bits

        'Checksum':0b0000000000000000,

        'Source':0x0, #4bytes

        'Dest':0x0, #4bytes
    }

    # Assuming the usage of 111.111.111.111 string format
    if(LOCAL_ADDRESS in not_allowed):
        print("Bad source address, \"{}\"".format(LOCAL_ADDRESS))
    elif(dest_address in not_allowed):
        print("Bad destination address, \"{}\"".format(dest_address))

    # Convert IP addresses to bytearrays
    header['Source'] = bytes(map(int, LOCAL_ADDRESS.split(".")))
    header['Dest'] = bytes(map(int, dest_address.split(".")))

    header_bytes = [
        ( ( (header['version'] << 4) + header['IHL']) << 8 ) + ( (header['DSCP'] << 2) + header['ECN'] ),
        header['TotLen'],
        header['Identification'],
        ((header['Flags'] << 13) + (header['Fragment Offset'])),
        (header['TTL'] << 8) + header['Protocol'],
        header['Checksum'],
        header['Source'] & 0xFFFF,
        header['Dest']
    ]

    """ # Debug
    #Verify header
    print([hex(x) for x in header_bytes])
    """

    # Checksum = index of checksum in header_bytes (should not be included in calculation)
    checksum = 5
    for i, value in enumerate(header_bytes):
        if(i != checksum):

            """ # Debug
            print("Iteration: {} and length {}".format(i, len(bin(header_bytes[checksum]))))
            before = header_bytes[checksum]
            """

            header_bytes[checksum] = header_bytes[checksum] + value

            """ # Debug
            print('''\
                {:016b}
              + {:016b}
                ------------------
                {:016b}\n'''.format(before, value, header_bytes[checksum]))
            print("In hex: 0x{:04x} + 0x{:04x} = 0x{:04x}\n".format(before, value, header_bytes[checksum]))
            """

            # Carry bit
            if(len(bin(header_bytes[checksum])) > 17):
                if((header_bytes[checksum] >> 16) & 0x01 == 1):
                    print("carry bit")
                    header_bytes[checksum] = (header_bytes[checksum] ^ (1 << 16)) + 1
                else:
                    header_bytes[checksum] = header_bytes[checksum] & 0xFFFF

    payload = data

    packet = header_bytes.append(bytes(payload))

    return packet

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
    duration = 5000
    role = mode(sys.argv[0])
    count = 3

    while count:
        if(role == "BASE"):
            start = time.time()
            while(time.time() - start < duration):
                transmit(tx_radio, dest_addr)
        else:
            start = time.time()
            receive(rx_radio, duration)
        count -= 1
