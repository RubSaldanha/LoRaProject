INITIAL_STATE = 0 # waiting for the first message
TRANSFER_STATE = 1 # waiting to receive packet with End
END_STATE = - 1




# When in INITIAL_STATE Receiving a begin mesage the state is updated to TRANSFER_STATE
# if timeout occurs in TRANSFER_STATE go to INITIAL_STATE
# if end packet is received go to INITIAL_STATE ?


def error_routine():
    pycom.rgbled(0xff0000) # Red led
    time.sleep(10)
    sys.exit(-1)

def show_packet_success():
    pycom.rgbled(0x00ff00) # verde led
    time.sleep(0.3)
    pycom.rgbled(0xf7f701)



pycom.rgbled(0xf7f701)
state = INITIAL_STATE

packet = b''
while True:

    while state == INITIAL_STATE:
        try:
            packet = s.recv(240)
            fname = str(packet)[8:] # first bytes are saying "Begin" supposedly
            print(fname)
            show_packet_success()
            state = TRANSFER_STATE
        except Exception as e:
            print(e)
            error_routine()
    start_time = time.time()


    if state == END_STATE:
        error_routine()

    fname = [char for char in fname if char.isalpha() or char == "."]
    fname ="".join(fname)
    fname = fname
    ini_time = time.time()
    i = 0
    with open ('/sd/' + fname + '_rcv', "wb") as f:
        while state == TRANSFER_STATE:
            try:
                packet = s.recv(240)
                print("packet " + str(i) + " time: " + str(ini_time-time.time()))
                ini_time = time.time()
                s.send(b'ACK')
                show_packet_success()
                i = i +1
                #print(packet)

                if b'End' in packet:
                    print("Total time of execution: ", time.time()-start_time)
                    state = INITIAL_STATE
                    pycom.rgbled(0xf7f701)
                else:
                    f.write(packet)

            except Exception as e:
                print(e)
                error_routine()
