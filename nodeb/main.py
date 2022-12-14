import os
from network import LoRa
import socket
import time
from machine import SD

# check the content
# Please pick the region that matches where you are using the device

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
i = 0
f = open('/sd/imageres.jpg', 'wb')
a = s.recv(240)
while a != b'End':
    if(a!=b''):
        print(a)
        f.write(a)
    a = s.recv(240)
    time.sleep(1)
f.close()
print("Acabou")
