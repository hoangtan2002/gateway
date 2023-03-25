import sys
import time
import random
from uart import *
from MQTT import *
#INFO

numOfConnectionTry = 0
state = 1

while numOfConnectionTry < 3 and state == 1:
    print('Connect Attempt Number'+str(numOfConnectionTry))
    state = connectSerial()
    if state == 1:
        numOfConnectionTry = numOfConnectionTry+1
        time.sleep(10)

if state == 1:
    client.publish("sensor03","MCU ISSUE")
    exit(1)
    
curTime = time.process_time()

while True:
    if time.process_time() - curTime >= 10 :
        writeData('!RST#')
        curTime = time.process_time()
    if readSerial(client):
        break
    pass