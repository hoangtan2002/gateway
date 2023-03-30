import serial.tools.list_ports
from log import * 
from writecsv import *

INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=2
MCU_MAX_CONNECT_ATTEMP=3
global state
prevTemp = 0
prevHumid = 0
currentTemp = 0
currentHumid = 0
isCollectedData = 0

def getIsCollectedData():
    return isCollectedData

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "ttyUSB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

def connectSerial():
    global state, ser
    ttyPort = getPort()
    if ttyPort!="None":
        try:
            ser = serial.Serial(port=ttyPort, baudrate=9600)
        except:
            return MCU_DISCONNECTED
        writelog("MCU CONNECTED!")
        print(ser)
        return MCU_CONNECTED
    else:
        writelog("CONNECTION ISSUE!")
        return MCU_DISCONNECTED
        
mess = ""

def readSerial(client):
    try:
        bytesToRead = ser.inWaiting()
    except:
        client.publish('duytan2002/feeds/sensor03',"MCU DISCONNECTED")
        return MCU_DISCONNECTED
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
    return MCU_CONNECTED
                
def processData(client, data):
    global prevTemp, prevHumid, isCollectedData, currentTemp, currentHumid
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if len(splitData) < 2:
        return
    if splitData[1]=='T':
        currentTemp = float(splitData[2])
        if currentTemp < 50:
            writelog(("Temp: " + str(currentTemp)))
            isCollectedData += 1
            if(prevTemp != currentTemp):
                prevTemp = currentTemp
                client.publish("duytan2002/feeds/sensor01", str(currentTemp))
            else:
                writelog("Same temp data")
                print("Same Temp data")
        else:
            print("SENSOR ISSUE!")
            writelog("SENSOR ISSUE")
    elif splitData[1]=='H':
        currentHumid = float(splitData[2])
        if currentHumid <= 100:
            writelog(("Humid: " + str(splitData[2])))
            isCollectedData += 1
            if(prevHumid != currentHumid):
                prevHumid = currentHumid
                client.publish("duytan2002/feeds/sensor02", str(currentHumid))
            else:
                print("Same humid data")
        else:
            print("SENSOR ISSUE!")
            writelog("SENSOR ISSUE") 
    if(isCollectedData==2):
        writelog("2 data point collected")
        writecsv(currentHumid, currentTemp)
        isCollectedData=0
        writeData('!OK#')

def writeData(data):
    ser.write(str(data).encode())
