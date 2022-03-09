import numpy as np
import struct
import random

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
        print(bytes(padding))
        #Add length of padding in the last byte
        print("Number of padding bytes = {}".format(len(padding)))
        padding[len(padding) - 1] += len(padding)
        data += bytes(padding)
        print("Data = {}".format(bytearray(data)))

    #Insert in numpy array and reshape into chunk_size B clusters
    fragmented = np.array(bytearray(data)).reshape(nbr_chunks, chunk_size)

    return fragmented


if __name__ == '__main__':
    data = [random.randint(0, 255) for _ in range(1000)]
    print(bytes(data))
    print('\n')
    print(fragment(bytes(data)))
