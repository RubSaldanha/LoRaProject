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
ini_time = time.time()
data = open("/sd/data.txt","a")
while True:
    i = 0
    data.write("\nNew image\n")
    while state == INITIAL_STATE:
        try:
            packet = s.recv(248)
            fname = str(packet)[8:] # first bytes are saying "Begin" supposedly
            #print(fname)
            data.write("packet " + str(i) + " time: 0\n")
            print("packet " + str(i) + " time: 0")
            i = 1
            ini_time = time.time()
            show_packet_success()
            state = TRANSFER_STATE
        except Exception as e:
            print(e)
            data.close()
            error_routine()

    start_time = time.time()


    if state == END_STATE:
        error_routine()

    fname = [char for char in fname if char.isalpha() or char == "."]
    fname ="".join(fname)
    last_cont = 0
    #print(fname)
    with open ('/sd/rcv_' + fname, "wb") as f:
        while state == TRANSFER_STATE:
            try:
                iden_cont = int.from_bytes(s.recv(1), "big")
                packet = s.recv(252)
                data.write("packet " + str(iden_cont) + " time: " + str(time.time()-ini_time) + "\n")
                print("packet " + str(iden_cont) + " time: " + str(time.time()-ini_time))
                ini_time = time.time()
                s.send(b'ACK')
                show_packet_success()
                i += 1
                #print(packet)

                if b'End' in packet:
                    #print(packet)
                    data.write("Total time of execution: " + str(time.time()-start_time) + "\n")
                    print("Total time of execution: " + str(time.time()-start_time))
                    state = INITIAL_STATE
                    pycom.rgbled(0xf7f701)
                else:
                    if iden_cont == (last_cont+1):
                        f.write(packet)
                        #print(packet)
                        last_cont = iden_cont

            except Exception as e:
                print(e)
                data.close()
                error_routine()
