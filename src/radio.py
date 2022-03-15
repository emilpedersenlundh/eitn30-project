#!/home/fideloper/.envs/eitn30-project/bin/python3

from RF24 import RF24, RF24_PA_LOW, RF24_PA_MAX, RF24_2MBPS, RF24_CRC_DISABLED, RF24_CRC_8, RF24_CRC_16

import utilities as util

SPI0 = {
    'SPI':0,
    'MOSI':10,
    'MISO':9,
    'clock':11,
    'ce':17,
    'csn':8
    }
SPI1 = {
    'SPI':10,
    'MOSI':20,
    'MISO':19,
    'clock':21,
    'ce':27,
    'csn':18
    }

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6"
]

SPI_SPEED = 10000000 #Hz
CHANNEL = 76 #2.4G + channel Hz
A_WIDTH = 5 #2-5 bytes
RT_DELAY = 0 #0-15 (250-4000 microseconds)
RT_LIMIT = 15 #0-15 (0 = Disabled)

class Radio:

    def __init__(self, mode):
        self.tx_radio = RF24(SPI0['ce'], SPI0['SPI'])
        self.rx_radio = RF24(SPI1['ce'], SPI1['SPI'])
        self.setup(self.tx_radio, mode)
        self.setup(self.rx_radio, mode)

    def setup(self, radio, mode):
        """
        Starts radio module and applies settings.
        """
        if not radio.begin():
            radio.printPrettyDetails()
            raise RuntimeError("Radio module is inactive.")

        # Set power amplifier level
        radio.setPALevel(RF24_PA_LOW)

        # Set payload size (dynamic/static)
        radio.enableDynamicPayloads()

        # Set CRC encoding
        radio.setCRCLength(RF24_CRC_16)

        # Set CRC enable/disable
        #radio.disableCRC()

        # Set auto-ACK (If false: CRC has to be disabled)
        radio.setAutoAck(True)

        # Set address A_WIDTH
        radio.setAddressWidth(A_WIDTH)

        # Set auto-retransmit delay & limit
        radio.setRetries(RT_DELAY, RT_LIMIT)

        # Set channel
        radio.setChannel(CHANNEL)

        # Set data rate
        radio.setDataRate(RF24_2MBPS)

        # Open pipes
        for pipe, address in enumerate(PIPE_ADDRESSES):
            if(mode == "NODE"):
                radio.openReadingPipe(pipe, address)
                print("Opened reading pipe: {} with address: {}".format(pipe, address))
        radio.openWritingPipe(PIPE_ADDRESSES[0])
        print("Opened writing pipe with address: {}".format(address))

        # Flush buffers
        radio.flush_rx()
        radio.flush_tx()

    def transmit(self, data) -> bool:
        #if data.size>mtu: data = util.fragment(data)
        pass

    def receive(self) -> bytes:
        pass
