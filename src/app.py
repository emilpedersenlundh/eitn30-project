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

from RF24 import RF24
from RF24 import RF24_PA_LOW, RF24_PA_MAX, RF24_2MBPS, RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16

SPI_SPEED: c_uint32 = 10000000 #Hz
CHANNEL: c_uint8 = 76 #2.4G + channel Hz
A_WIDTH: c_uint8 = 5 #2-5 bytes
RT_DELAY: c_uint8 = 0 #0-15 (250-4000 microseconds)
RT_LIMIT: c_uint8 = 15 #0-15 (0 = Disabled)

#6 slots for addresses
IP_TABLE = np.array([1 for _ in range(6)])

LOCAL_ADDRESS = []

#Data buffer for all pipes in rx (128 bytes)
DATA_BUFFER = np.array([[] for _ in range(len(IP_TABLE))])

#Config value arrays

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
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]

"""
PIPE_ADDRESSES = [
    b"\x78" * 5,
    b"\xF1\xB6\xB5\xB4\xB3",
    b"\xCD\xB6\xB5\xB4\xB3",
    b"\xA3\xB6\xB5\xB4\xB3",
    b"\x0F\xB6\xB5\xB4\xB3",
    b"\x05\xB6\xB5\xB4\xB3"
]
"""

#tx_radio = RF24(SPI0['SPI'],SPI0['csn'], SPI0['ce'], SPI_SPEED)
#rx_radio = RF24(SPI1['SPI'],SPI1['csn'], SPI1['ce'], SPI_SPEED)
#tx_radio = RF24(SPI0['ce'], SPI0['csn'], SPI_SPEED)
#rx_radio = RF24(SPI1['ce'], SPI1['csn'], SPI_SPEED)
#tx_radio = RF24(17, 0)
#rx_radio = RF24(27, 10)


# Declare radio objects
tx_radio = RF24(SPI0['ce'], SPI0['SPI'])
rx_radio = RF24(SPI1['ce'], SPI1['SPI'])

# Functions
def setup(mode_select: str="NODE"):

    # Initialize radio, if error: return runtime error
    if not rx_radio.begin():
        rx_radio.printPrettyDetails()
        raise RuntimeError("RX Radio is inactive.")

    if not tx_radio.begin():
        tx_radio.printPrettyDetails()
        raise RuntimeError("TX Radio is inactive.")

    # Set power amplifier level
    rx_radio.setPALevel(RF24_PA_LOW)
    tx_radio.setPALevel(RF24_PA_LOW)

    # Set payload size (dynamic/static)
    rx_radio.enableDynamicPayloads()
    tx_radio.enableDynamicPayloads()

    # Set CRC encoding
    rx_radio.setCRCLength(RF24_CRC_16)
    tx_radio.setCRCLength(RF24_CRC_16)

    # Set CRC enable/disable
    #rx_radio.disableCRC()
    #tx_radio.disableCRC()

    # Set auto-ACK (If false: CRC has to be disabled)
    rx_radio.setAutoAck(True)
    tx_radio.setAutoAck(True)

    # Set address A_WIDTH
    rx_radio.setAddressWidth(A_WIDTH)
    tx_radio.setAddressWidth(A_WIDTH)

    # Set auto-retransmit delay & limit
    rx_radio.setRetries(RT_DELAY, RT_LIMIT)
    tx_radio.setRetries(RT_DELAY, RT_LIMIT)

    # Set channel
    rx_radio.setChannel(CHANNEL)
    tx_radio.setChannel(CHANNEL)

    # Set data rate
    rx_radio.setDataRate(RF24_2MBPS)
    tx_radio.setDataRate(RF24_2MBPS)

    # Open pipes
    for pipe, address in enumerate(PIPE_ADDRESSES):
        if(mode_select == "NODE"):
            rx_radio.openReadingPipe(pipe, address)
            print("Opened reading pipe: {} with address: {}".format(pipe, address))
    tx_radio.openWritingPipe(PIPE_ADDRESSES[0])
    print("Opened writing pipe with address: {}".format(address))

    # Flush buffers
    rx_radio.flush_rx()
    rx_radio.flush_tx()
    tx_radio.flush_rx()
    tx_radio.flush_tx()

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

    tx_radio.stopListening()
    start = time.monotonic()
    while count:
        # use struct.pack to packetize your data
        # into a usable payload

        buffer = struct.pack("<i", count)
        # 'i' means a single 4 byte int value.
        # '<' means little endian byte order. this may be optional
        print("Sending: {} as struct: {}".format(count, buffer))
        result = tx_radio.write(buffer, False)
        if not result:
            print("send() failed or timed out")
            #tx_radio.whatHappened()
            status.append(False)
        else:
            print("send() successful")
            status.append(True)
        # print timer results despite transmission success
        count -= 1
    total_time = time.monotonic() - start

    print('{} successful transmissions, {} failures, {} bps\n'.format(sum(status), len(status)-sum(status), size*8*len(status)/total_time))

def receive(rx_radio, timeout):

    print('Rx NRF24L01+ started w/ power {}, SPI freq: {}hz'.format(rx_radio.getPALevel(), SPI_SPEED))

    # Start listening
    rx_radio.startListening()
    start = time.time()
    # Timeout condition
    while(time.time() - start < timeout):

        #Checks if there are bytes available for read
        payload_available, pipe_nbr = rx_radio.available_pipe()

        if(payload_available):

            print("Payload available = {} \nPipe number = {}".format(payload_available, pipe_nbr))
            # If has payload, read radio packet size
            payload_size = rx_radio.getDynamicPayloadSize()
            payload = struct.unpack("<i", rx_radio.read(payload_size))
            print("Payload size = {} \nPayload = {}".format(payload_size, np.ravel(np.array(payload))))

            # Insert payload into data buffer
            DATA_BUFFER[pipe_nbr] = np.array([payload])
            print("Received a payload in pipe {} of size {} bytes and data {}\n".format(pipe_nbr, payload_size, np.ravel(DATA_BUFFER[pipe_nbr])))

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
    print(userinput)
    if userinput == "BASE" or userinput == "NODE":
        mode = userinput
    else:
        print("No mode specified, defaulting to NODE..")
        mode = "NODE"
    print("Role = {}".format(mode))
    return mode

if __name__ == "__main__":

    mode_select = input("Select mode (BASE or NODE): ").upper()

    setup(mode_select)
    dest_addr = 1
    duration = 5000
    role = mode(mode_select)
    count = 3
try:
    while count:
        if(role == "BASE"):
            start = time.time()
            while(time.time() - start < duration):
                transmit(tx_radio, dest_addr)
        else:
            start = time.time()
            receive(rx_radio, duration)
        count -= 1

except KeyboardInterrupt:
    print("\n----Keyboard interrupt----\n")
    if (role == "NODE"):
        print("RX Radio Details: \n")
        rx_radio.printPrettyDetails()
    if (role == "BASE"):
        print("\nTX Radio Details:\n")
        tx_radio.printPrettyDetails()
