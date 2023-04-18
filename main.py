import sys
import time
import random
from uart import *
from MQTT import *
from recognitionAI import *
from predictAI import *
#INFO

sendPeriod = 10
INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=2
state = INIT
curTime = time.process_time()
aiTime = time.process_time()
WAIT = 5      
predictTime = time.process_time()
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
    if time.process_time() - aiTime > 30:
        aiResult = SuperAI()
        if(aiResult!=""):
            client.publish("duytan2002/feeds/ai", aiResult)
        aiTime = time.process_time()
    if time.process_time() - predictTime > 45:
        predictedTemp, predictedHumid = predict()
        client.publish("duytan2002/feeds/predictedtemp",predictedTemp)
        client.publish("duytan2002/feeds/predictedhumid",predictedHumid)
        predictTime = time.process_time()
    pass
