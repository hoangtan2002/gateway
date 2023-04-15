#from Adafruit_IO import MQTTClient
import paho.mqtt.client as mqtt
import sys
from uart import *

KEYFILE = open("./keyed_file", "r")
AIO_FEED_ID = ["button01", "button02", "freq"]
AIO_USERNAME = KEYFILE.readline().strip()
AIO_KEY = KEYFILE.readline().strip()
#CONSTANT
isConnectedSuccessfully = 0
sendPeriod = 10

for i in range(len(AIO_FEED_ID)):
    AIO_FEED_ID[i]= AIO_USERNAME+"/feeds/"+AIO_FEED_ID[i]

print(AIO_FEED_ID)
def isConnected():
    return isConnectedSuccessfully

def getSendPeriod():
    return sendPeriod

def connected(client, userdata, flags, rc):
    global isConnectedSuccessfully
    for topic in AIO_FEED_ID:
        client.subscribe(topic)
    print(flags)
    print(rc)
    print("Ket noi thanh cong ...")
    isConnectedSuccessfully = 1
    client.publish("duytan2002/feeds/freq", str(sendPeriod))
    

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client, userdata, rc):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , userdata, message):
    global sendPeriod
    decodedPayload = message.payload.decode()
    print("Nhan du lieu: " + decodedPayload + " type" + str(type(decodedPayload)))
    if "button01" in  message.topic:
        if  decodedPayload == '0':
            writeData("!OFF1#")
        else: 
            writeData("!ON1#")
    if "button02" in message.topic:
        if  decodedPayload == '0':
            writeData("!OFF2#")
        else: 
            writeData("!ON2#")
    if "freq" in message.topic:
        sendPeriod = int(decodedPayload)
        print("New send period: " + decodedPayload)

client = mqtt.Client()
client.username_pw_set(username=AIO_USERNAME, password=AIO_KEY)
client.will_set("duytan2002/feeds/connectcheck", payload=0, qos=0, retain=True)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
try:
    client.connect("io.adafruit.com", 1883, 10)
except:
    writelog("NO INTERNET CONNECTION")
    exit(1)
client.loop_start()