import sys
import time
import random
from uart import *
from MQTT import *
#INFO

numOfConnectionTry = 0
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
        while numOfConnectionTry < MCU_MAX_CONNECT_ATTEMP and state != MCU_CONNECTED:
            if time.process_time()-curTime > 3: 
                print('Connect Attempt Number:'+str(numOfConnectionTry))
                state = connectSerial()
                if state == INIT or state == MCU_DISCONNECTED:
                    numOfConnectionTry = numOfConnectionTry+1
                else: 
                    numOfConnectionTry = 0
        if numOfConnectionTry == MCU_MAX_CONNECT_ATTEMP:
            client.publish("sensor03","MCU ISSUE")
            sys.exit(1)
    if state == MCU_CONNECTED:
        if time.process_time() - curTime >= sendPeriod :
            writeData('!RST#')
            curTime = time.process_time()
            sendPeriod = getSendPeriod()
            sendPeriod = getSendPeriod()
    state=readSerial(client)
    pass