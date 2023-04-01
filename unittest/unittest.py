import unittest
import time
from MQTT import *
from uart import *

def uartTest():
    print("Plug in MCU and chmod now")
    time.sleep(15)
    connectAttemp()
    writeData('!RST#')
    state = readSerial()
    print(state)

uartTest()