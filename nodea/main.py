import os
import sys
from network import LoRa
import socket
import time

# check the content
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

BLOCKSIZE=240 # read atmost 240 bytes




def read_blocks(figure):
    fd = open(figure, "rb")
    #print(s)
    bytes_read = 0      # overall bytes read (debug)
    eofflag = 0         # 1 means end of file
    bytes_read_iter = 0 # byte read in the outermost while loop

    while True:

        buffer_in = fd.read(BLOCKSIZE)

        # EOF
        if buffer_in == b'':
            print("EOF")
            break

        bytes_read_iter = len(buffer_in)
        print(bytes_read_iter)
        print()

        # while loop that assures that BLOCKSIZE was read:
        while bytes_read_iter != BLOCKSIZE and not eofflag:
            buffer_in += fd.read(BLOCKSIZE - bytes_read_iter)

            if len(buffer_in) - bytes_read_iter == 0: # nothing more was read therefore EOF
                eofflag = 1



        print(buffer_in)
        s.send(buffer_in)
        print()
        bytes_read += len(buffer_in)
        time.sleep(5)
        if eofflag:
            print("EOF")
            s.send('End')
            break

    fd.close()
    print(bytes_read)

read_blocks("/sd/image.jpg")
read_blocks("/sd/image1.jpg")
#if __name__ == "__main__":
#    read_blocks("testimage.jpg")
