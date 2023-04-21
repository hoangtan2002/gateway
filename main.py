import sys
import time
from uart import *
from MQTT import *
from recognitionAI import *
from predictAI import *
import threading
#INFO

sendPeriod = 10
INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=2
state = INIT
HOPELESS=99
curTime = time.process_time()
aiTime = time.process_time()
WAIT = 5      
predictTime = time.process_time()
time.sleep(WAIT)

predictAIevent = threading.Event()
predictAIThread = threading.Thread(target=lambda:predictionMainloop(predictAIevent))
predictAIThread.start()

recognitionAiEvent = threading.Event()
recognitionAiThread = threading.Thread(target=lambda:recognitionAiMainLoop(recognitionAiEvent))
recognitionAiThread.start()
        
while True:  
    if state == INIT or state == MCU_DISCONNECTED:
        state = connectAttemp(state, client)
    if state == MCU_CONNECTED:
        if time.process_time() - curTime >= sendPeriod :
            writeData('!RST#')
            curTime = time.process_time()
    if state == HOPELESS:
        recognitionAiEvent.set()
        predictAIevent.set()
        sys.exit(1)
    sendPeriod = getSendPeriod()
    state=readSerial(client)
    pass
