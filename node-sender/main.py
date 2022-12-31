
BLOCKSIZE=250 # read atmost 240 bytes
LIMIT_TIMEOUTS = 3
def error_routine():
    pycom.rgbled(0xff0000) # Red led
    time.sleep(0.1)
    pycom.rgbled(0xf7f701)
    time.sleep(5)
    #sys.exit(-1)

def show_packet_success():
    pycom.rgbled(0x00ff00) # green led

def read_blocks(figure):
    timeouts = 0
    lost_packets = 0
    pycom.rgbled(0xf7f701)
    fd = open(figure, "rb")
    s.send(bytes('Begin {}'.format(figure.split("/")[-1]) , 'utf-8'))

    try:
        s.recv(10)
        show_packet_success()
    except Exception as e:
        print(e)
        timeouts += 1
        lost_packets = lost_packets +1
        error_routine()

    time.sleep(5)
    bytes_read = 0      # overall bytes read (debug)
    eofflag = 0         # 1 means end of file
    bytes_read_iter = 0 # byte read in the outermost while loop
    resend_packet = 0
    i = 1
    while True:
        if resend_packet == 0:
            buffer_in = fd.read(BLOCKSIZE-1)
            timeouts = 0

            if buffer_in == b'':
                #print("EOF1")

                buffer_in = int(0).to_bytes(1, 'big') + b'End'
                s.send(buffer_in)
                break
            else:
                buffer_in = i.to_bytes(1, 'big') + buffer_in
                i += 1
                #print(buffer_in)

            bytes_read_iter = len(buffer_in)
            #print(bytes_read_iter)
            #print()

            # while loop that assures that BLOCKSIZE was read:
            while bytes_read_iter != BLOCKSIZE and not eofflag:
                buffer_in += fd.read(BLOCKSIZE - bytes_read_iter)

                if len(buffer_in) - bytes_read_iter == 0: # nothing more was read therefore EOF
                    eofflag = 1
        #print(buffer_in)
        s.send(buffer_in)
        try:
            s.recv(10)
            resend_packet = 0
            show_packet_success()
        except Exception as e:
            print(e)
            resend_packet = 1
            timeouts += 1
            lost_packets = lost_packets +1
            error_routine()

        if timeouts == LIMIT_TIMEOUTS:
            print("lost packets:" + str(lost_packets))
            sys.exit(-1)

        #print()
        bytes_read += len(buffer_in)
        time.sleep(5)
        if eofflag:
            #print("EOF2")
            #s.send('End')S
            eof_msg = int(0).to_bytes(1, 'big') + b'End'
            s.send(eof_msg)
            break

    fd.close()
    return lost_packets
    #print(bytes_read)

imgs = ["/sd/testimage.jpg","/sd/testimage1.jpg", "/sd/testimage2.jpg","/sd/testimage3.jpg"]
for img in imgs:
    print("Image " + img)
    lost_packets = read_blocks(img)
    pycom.rgbled(0x000000)
    time.sleep(0.4)
    print("lost packets:" + str(lost_packets))

#read_blocks("/sd/image1.jpg")
#if __name__ == "__main__":
#    read_blocks("testimage.jpg")
