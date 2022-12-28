# boot.py -- run on boot-up
# RECEIVER

from network import LoRa
from machine import SD
import os
import socket
from socket import AF_LORA, SOCK_RAW
import pycom
import sys
import time


pycom.heartbeat(False)

#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7, preamble=8)
lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ, sf=10, preamble=8)
#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=10, preamble=8)
#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ, sf=7, preamble=8)

#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7, preamble=8)
#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7, preamble=8)
#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7, preamble=8)
#lora = LoRa(mode = LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7, preamble=8)

if '/sd' in os.listdir('/'):
    os.umount('/sd')

sd = SD()
os.mount(sd, '/sd')


s = socket.socket(AF_LORA, SOCK_RAW)
s.setblocking(True)
s.settimeout(10)
