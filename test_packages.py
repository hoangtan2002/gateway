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