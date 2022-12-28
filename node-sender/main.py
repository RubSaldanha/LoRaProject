def error_routine():
    pycom.rgbled(0xff0000) # Red led
    time.sleep(0.1)
    pycom.rgbled(0xf7f701)
    time.sleep(5)
    #sys.exit(-1)

def show_packet_success():
    pycom.rgbled(0x00ff00) # green led

BLOCKSIZE=240 # read atmost 240 bytes
LIMIT_TIMEOUTS = 3

timeouts = 0

def read_blocks(figure):
    pycom.rgbled(0xf7f701)
    fd = open(figure, "rb")
    s.send(bytes('Begin {}'.format(figure.split("/")[-1]) , 'utf-8'))
    #print(s)
    bytes_read = 0      # overall bytes read (debug)
    eofflag = 0         # 1 means end of file
    bytes_read_iter = 0 # byte read in the outermost while loop
    resend_packet = 0
    while True:
        if resend_packet == 0:
            buffer_in = fd.read(BLOCKSIZE)
            timeouts = 0

            if buffer_in == b'':
                print("EOF")
                s.send(bytes('End'.format(bytes_read)))
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
        try:
            s.recv(10)
            resend_packet = 0
            show_packet_success()
        except Exception as e:
            print(e)
            resend_packet = 1
            timeouts += 1
            error_routine()
        if timeouts == LIMIT_TIMEOUTS:
            return

        print()
        bytes_read += len(buffer_in)
        time.sleep(5)
        if eofflag:
            print("EOF")
            #s.send('End')
            s.send(bytes('End', 'utf-8'))
            break

    fd.close()
    print(bytes_read)

read_blocks("/sd/testimage.jpg")
pycom.rgbled(0x000000)
#read_blocks("/sd/image1.jpg")
#if __name__ == "__main__":
#    read_blocks("testimage.jpg")
