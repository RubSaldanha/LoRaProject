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

data = open("/sd/data_16-500.txt","a")
while True:
    ini_time = time.time()
    i = 0
    while state == INITIAL_STATE:
        ini_time = time.time()
        try:
            packet = s.recv(252)
            if(packet == b''):
                break;
            fname = str(packet)[8:] # first bytes are saying "Begin" supposedly
            data.write("\n" + fname + "\n")
            data.write("packet " + str(i) + " time: 0\n")
            s.send(b'ACK')
            show_packet_success()
            #print("packet " + str(i) + " time: 0")
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

    fname = [char for char in fname if char.isalpha() or char == "." or char.isdigit()]
    fname ="".join(fname)
    print(fname)
    last_cont = 0
    with open ('/sd/16-500_rcv_' + fname, "wb") as f:
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
