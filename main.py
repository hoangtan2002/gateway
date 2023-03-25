import sys
import time
import random
from uart import *
from MQTT import *
#INFO

numOfConnectionTry = 0

INIT=0
MCU_CONNECTED=1
state = INIT

while numOfConnectionTry < 3 and state == INIT:
    print('Connect Attempt Number'+str(numOfConnectionTry))
    state = connectSerial()
    if state == INIT:
        numOfConnectionTry = numOfConnectionTry+1
        time.sleep(10)

if state == INIT:
    client.publish("sensor03","MCU ISSUE")
    exit(1)
    
curTime = time.process_time()

while True:
    if time.process_time() - curTime >= 10 :
        writeData('!RST#')
        curTime = time.process_time()
    if readSerial(client)==MCU_DISCONNECTED:
        break
    pass