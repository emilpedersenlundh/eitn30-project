#!/home/fideloper/.envs/eitn30-project/bin/python3
import numpy as np

# Data handling
def fragment(data) -> list:

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

def mode(userinput: str=""):
    
    mode = ""
    print(userinput)
    if userinput == "BASE" or userinput == "NODE":
        mode = userinput
        print("Role = {}".format(mode))
    else:
        print("No mode specified, defaulting to NODE..")
        mode = "NODE"
    return mode

# Status tools
def status(parameters: dict):
    """
    Prints a status bar in the terminal. Parameters should be structured as status_type:status_value.
    """
    message = ''
    for key in parameters:
        message += "{}: {}| ".format(key, parameters(key))
    print(message, end='\r')
