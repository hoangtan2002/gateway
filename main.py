import sys
import time
import random
from uart import *
from MQTT import *
#INFO

numOfConnectionTry = 0
sendPeriod=10
INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=0
state = INIT
curTime = time.process_time()
        
while True:
    if state == INIT or state == MCU_DISCONNECTED:
        if(state==MCU_DISCONNECTED):
            client.publish("sensor03", "MCU DISCONNECTED")
            writelog("MCU DISCONNECTED")
        print('Connect Attempt Number:'+str(numOfConnectionTry))
        state = connectSerial()
        if state == INIT or state == MCU_DISCONNECTED:
            numOfConnectionTry = numOfConnectionTry+1
        time.sleep(3)
        if numOfConnectionTry == MCU_MAX_CONNECT_ATTEMP:
            sys.exit(1)
    elif state == MCU_CONNECTED:    
        if time.process_time() - curTime >= sendPeriod :
            writeData('!RST#')
            curTime = time.process_time()
            sendPeriod = getSendPeriod()
            state = readSerial(client)
    pass