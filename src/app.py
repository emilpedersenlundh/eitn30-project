#!/home/fideloper/.envs/eitn30-project/bin/python3

import array
from ctypes import c_byte, c_uint, c_uint16, c_uint32, c_uint8
import sys
import argparse
import time
import struct
import random
import typing
import numpy as np

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
data_buffer = [[] for _ in range(len(IP_TABLE))]

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
# TODO fix addresses to big endian
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

def fragment(data):

    nbr_chunks = 0
    data_length = len(data)
    """
    Chunk size < 32 to have space for an id byte when sending
    if 31 is used, 1B can be used as id -> Able to send 256 * 31 = 7936B in total, if 30 is used id=2B 65536 * 30 = 1966080B can be sent
    """
    chunk_size = 30

    if((data_length % chunk_size) == 0):
        nbr_chunks = data_length / chunk_size
    else:
        nbr_chunks = int((data_length - (data_length % chunk_size)) / chunk_size) + 1

        #Padding with zeroes followed by padding size (max chunk_size  - 1 B)
        padding = [0 for _ in range(chunk_size - (data_length % chunk_size))]
        #print(bytes(padding))
        #Add length of padding in the last byte
        #print("Number of padding bytes = {}".format(len(padding)))
        padding[len(padding) - 1] += len(padding)
        data += bytes(padding)
        #print("Data = {}".format(bytearray(data)))

    #Insert in numpy array and reshape into nbr_chunks clusters of size chunk_size
    fragmented = np.array(bytearray(data)).reshape(nbr_chunks, chunk_size)

    return fragmented.tolist()

# @TODO How do we handle addresses etc in L2? do we need to?
def transmit(tx_radio, address):

    time.sleep(5) #To power up node in time

    status = []
    data = bytes([random.randint(0, 255) for _ in range(100)])

    #Fragment the data into chunks (n chunks * chunk size (30) matrix, each line is a chunk)
    if(len(data) > 30):
        chunks = fragment(data)
    else:
        chunks = list(data)

    tx_radio.stopListening()

    start = time.monotonic()
    if(len(chunks) != 0):

        #If it has only 1 row, then id = 0x0000
        if(len(chunks) == 1):

            id = 0
            print("id = {}, and as struct = {}".format(id, struct.pack("<H", id)))

            chunk.append(struct.pack("<H", id))
            buffer = bytes(chunk)

            print("Sending: {} as struct: {}".format(chunk, buffer))
            result = tx_radio.write(buffer, False)

            if not result:
                print("send() failed or timed out")
                status.append(False)
            else:
                print("send() successful")
                status.append(True)

        #Otherwise send all available chunks and append id > 0
        else:

            id = 1
            nbr_chunks = len(chunks)

            #Data available to send
            for index, chunk in enumerate(chunks):

                print("id = {}, and as struct = {}".format(id, struct.pack(">H", id)))

                #Last fragment part will have id 0
                if(index == len(chunks) - 1):
                    id = pow(2, 16) - 1 #0xFFFF

                buffer = bytes(chunk)
                buffer += struct.pack(">H", id)

                #Send all chunks one at a time
                print("Sending chunk {} of {} with data: {} as struct {}, ".format(id, nbr_chunks, chunk, buffer))
                result = tx_radio.write(buffer, False)

                if not result:
                    print("send() failed or timed out")
                    status.append(False)
                else:
                    print("send() successful")
                    status.append(True)

                id += 1
                #Reduce speed for debug
                time.sleep(1)

    total_time = time.monotonic() - start

    print('{} successful transmissions, {} failures, {} bps\n'.format(sum(status), len(status)-sum(status), nbr_chunks*len(chunks[0])*8*len(status)/total_time))

def receive(rx_radio, timeout):

    global data_buffer

    print('Rx NRF24L01+ started w/ power {}, SPI freq: {}hz'.format(rx_radio.getPALevel(), SPI_SPEED))

    nbr_pipes = len(IP_TABLE)
    fragmented = [False for _ in range(nbr_pipes)]
    fragment_buffer = [[] for _ in range(nbr_pipes)]
    id_offset = 2

    rx_radio.startListening()
    start = time.time()

    # Timeout condition
    while(time.time() - start < timeout):

        #Checks if there are bytes available for read
        payload_available, pipe_nbr = rx_radio.available_pipe()
        payload = []

        if(payload_available):

            print("Payload available = {} \nPipe number = {}".format(payload_available, pipe_nbr))
            # If has payload, read radio packet size
            payload_size = rx_radio.getDynamicPayloadSize()
            payload = rx_radio.read(payload_size)

            id = struct.unpack(">H", payload[payload_size - id_offset: payload_size])[0]
            print("id = {}".format(id))

            if(id == 1):

                #First fragment
                fragmented[pipe_nbr] = True
                print(bytes(payload[: payload_size - id_offset]))
                fragment_buffer[pipe_nbr].append(bytes(payload[: payload_size - id_offset]))
                print("Received first fragment (id: {}) \ndata = {}\n".format(id, fragment_buffer.pop()))

            elif(id > 0 and fragmented[pipe_nbr]):

                #Fragmented data
                print(bytes(payload[: payload_size - id_offset]))
                fragment_buffer[pipe_nbr].append(str(bytes(payload[: payload_size - id_offset])))
                print("Received fragment nbr: {} \ndata = {}\n".format(id, fragment_buffer[pipe_nbr].pop()))

            elif(id == 0):

                print("fragment_buffer = {}".format(fragment_buffer[pipe_nbr]))
                # Not fragmented, insert payload into data buffer and "push" fragment_buffer to data_buffer + clear fragment buff
                print("fragmented = {}, len buff = {}".format(fragmented[pipe_nbr], len(fragment_buffer[pipe_nbr])))

                if(fragmented[pipe_nbr] and len(fragment_buffer[pipe_nbr]) != 0):

                    #Last fragmented packet, remove id and padding
                    padding_size = payload[payload_size - id_offset - 1]
                    fragment_buffer.append(payload[:payload_size - padding_size - id_offset - 2]) #-4 to remove id bytes and padding size byte

                    #Add all fragments to one element in the global buffer
                    data_buffer[pipe_nbr].append([x for x in fragment_buffer])
                    fragment_buffer[pipe_nbr].clear()
                    print("All fragments received!")
                    fragmented[pipe_nbr] = False
                else:

                    #Normal packet not fragmented
                    fragmented[pipe_nbr] = False
                    data_buffer[pipe_nbr].append(bytes(payload[: payload_size - id_offset - 1]))
                    print("Received a payload in pipe {} \nsize {} bytes \ndata {}\n".format(pipe_nbr, payload_size, np.ravel(data_buffer[pipe_nbr].pop())))
            else:
                print("Fragmentation order corrupt (id: {}), discarding packet..".format(id))

            # Flush rx buffer
            #rx_radio.flush_rx()

            # Reset the timeout timer
            start = time.time()

    # Timeout
    print("Timeout")
    rx_radio.stopListening()

def construct_packet(dest_address: str, data: list, broadcast: bool = False):

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
        print("\nRX Radio Details:\n")
        rx_radio.printPrettyDetails()
    if (role == "BASE"):
        print("\nTX Radio Details:\n")
        tx_radio.printPrettyDetails()
