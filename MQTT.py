from Adafruit_IO import MQTTClient
import sys
from uart import *

KEYFILE = open("./keyed_file", "r")
AIO_FEED_ID = ["button01", "button02"]
AIO_USERNAME = KEYFILE.readline().strip()
AIO_KEY = KEYFILE.readline().strip()
#CONSTANT
isConnectedSuccessfully = 0

def isConnected():
    return isConnectedSuccessfully

def connected(client):
    global isConnectedSuccessfully
    for topic in AIO_FEED_ID:
        client.subscribe(topic)
    print("Ket noi thanh cong ...")
    isConnectedSuccessfully = 1

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if feed_id == "button01":
        if payload == "0":
            writeData("1")
        else: 
            writeData("2")
    if feed_id == "button02":
        if payload == "0":
            writeData("3")
        else: 
            writeData("4")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
try:
    client.connect()
except:
    writelog("NO INTERNET CONNECTION")
    exit(1)
client.loop_background()