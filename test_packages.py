

# class TestUartMethods(unittest.TestCase):
#     @patch('serial.tools.list_ports.comports')
#     def test_getPort(self, mock_comports):
#         message = "getPort test failed"
#         mock_comports.return_value = [serial.tools.list_ports.ListPortInfo(device='/dev/ttyUSB1', description='Arduino Uno')]
#         self.assertEqual(getPort(), '/dev/ttyUSB0', message)

#     @patch('serial.Serial')
#     def test_connectSerial(self, mock_Serial):
#         mock_Serial.return_value = MagicMock()
#         self.assertEqual(connectSerial(), MCU_CONNECTED)

#     @patch('serial.Serial')
#     def test_readSerial(self, mock_Serial):
#         mock_Serial.return_value = MagicMock()
#         mock_Serial.return_value.inWaiting.return_value = 10
#         mock_Serial.return_value.read.return_value = b'!OK#'
#         client = MagicMock()
#         self.assertEqual(readSerial(client), MCU_CONNECTED)

#     def test_checkIntegrity(self):
#         message = "getPort test failed"
#         self.assertEqual(checkIntegrity('!OK:25.0:50.0:145#'), 1, message)
#         self.assertEqual(checkIntegrity('!OK:25.0:50.0:146#'), 1, message)

#     @patch('time.process_time')
#     def test_connectAttemp(self, mock_process_time):
#         mock_process_time.side_effect = [0, 4, 8, 12]
#         global numOfConnectionTry
#         numOfConnectionTry = 0
#         client = MagicMock()
#         self.assertEqual(connectAttemp(MCU_DISCONNECTED, client), MCU_CONNECTED)
#         numOfConnectionTry = 0
#         self.assertEqual(connectAttemp(INIT, client), MCU_DISCONNECTED)
#         numOfConnectionTry = 3
#         self.assertEqual(connectAttemp(MCU_DISCONNECTED, client), MCU_DISCONNECTED)

#     def test_processData(self):
#         global prevTemp, prevHumid, isCollectedData, currentTemp, currentHumid
#         prevTemp = 0
#         prevHumid = 0
#         isCollectedData = False
#         currentTemp = 25.0
#         currentHumid = 50.0
#         client = MagicMock()
#         processData(client, '!OK:25.0:50.0:145#')
#         self.assertEqual(prevTemp, 25.0)
#         self.assertEqual(prevHumid, 50.0)
#         self.assertEqual(isCollectedData, True)

#     def test_getIsCollectedData(self):
#         global isCollectedData
#         isCollectedData = True
#         self.assertEqual(getIsCollectedData(), True)
        
# if __name__ == 'main':
#     unittest.main()


import unittest
from unittest.mock import patch, MagicMock
from uart import *
#from MQTT import *
import serial
import serial.tools.list_ports
import time
import sys
  
class TestStringMethods(unittest.TestCase):
    # test function to test equality of two value
    def test_checkIntegrity_True(self):
        message = "checkIntegrity failed"
        # assertEqual() to check equality of first & second value
        self.assertEqual(checkIntegrity('OK:28.00:68.00:770'), 1, message)
        self.assertEqual(checkIntegrity('OK:28.57:68.00:770'), 0, message)
  
if __name__ == '__main__':
    unittest.main()