import os
import sys
BLOCKSIZE=240 # read atmost 240 bytes

def read_blocks(fName):
    fd = open(fName, "rb")

    bytes_read = 0 #overall bytes read (debug)
    eofflag = 0 # 1 means end of file
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
        print()
        bytes_read += len(buffer_in)

        if eofflag:
            print("EOF")
            break

    fd.close()
    print(bytes_read)

if __name__ == "__main__":
    read_blocks(sys.argv[1])
