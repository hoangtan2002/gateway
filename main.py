import sys
import time
import random
from uart import *
from MQTT import *
#INFO

sendPeriod = 10
INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=2
state = INIT
curTime = time.process_time()
WAIT = 5      
# while not isConnected():
#     print()       
time.sleep(WAIT)
while True:  
    if state == INIT or state == MCU_DISCONNECTED:
        state = connectAttemp(state, client)
    if state == MCU_CONNECTED:
        if time.process_time() - curTime >= sendPeriod :
            writeData('!RST#')
            curTime = time.process_time()
    sendPeriod = getSendPeriod()
    state=readSerial(client)
    pass