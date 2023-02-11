import sys
from Adafruit_IO import MQTTClient
import time
import random
#from simple_ai import *
from uart import *
#INFO
KEYFILE = open("./keyed_file", "r")
AIO_FEED_ID = ["button01", "button02"]
AIO_USERNAME = KEYFILE.readline().strip()
AIO_KEY = KEYFILE.readline().strip()

def connected(client):
    for topic in AIO_FEED_ID:
        client.subscribe(topic)
    print("Ket noi thanh cong ...")

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
client.connect()
client.loop_background()

counter = 10

while True:
    #counter = counter - 1
    #if counter == 0: 
        # #Random val
        # #temp = random.randint(30,40)
        # #humid = random.randint(50, 80)
        # #lightval = random.randint(200, 400)
        #ai_result = SuperAI()
        # #publish val
        # client.publish("sensor01", temp)
        # client.publish("sensor02", humid)
        # client.publish("sensor03", lightval)
        # client.publish("ai", ai_result)
        #counter = 10
    readSerial(client)
    #
    #time.sleep(1)
    pass