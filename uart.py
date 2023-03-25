import serial.tools.list_ports
from log import * 
INIT=0
MCU_CONNECTED=1
MCU_DISCONNECTED=0
MCU_MAX_CONNECT_ATTEMP=3

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
            print(splitPort[0])
    return commPort

def connectSerial():
    global state, ser
    if getPort()!="None":
        ser = serial.Serial(port=getPort(), baudrate=9600)
        writelog("MCU CONNECTED!")
        print(ser)
        return MCU_CONNECTED
    else:
        writelog("CONNECTION ISSUE!")
        return INIT
        
mess = ""

def readSerial(client):
    try:
        bytesToRead = ser.inWaiting()
    except:
        client.publish("sensor03", "MCU DISCONNECTED")
        writelog("MCU DISCONNECTED")
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
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if len(splitData) < 2:
        return
    if splitData[1]=='T':
        if int(splitData[2]) < 50:
            writeData('!OK#')
            client.publish("sensor01", splitData[2])
            writelog((" Temp: " + str(splitData[2])))
        else:
            print("SENSOR ISSUE!")
            writelog("SENSOR ISSUE")
            
    # elif splitData[1]=='H':
    #     client.publish("sensor02", splitData[2])
    #     writelog((" Humidity: " + str(splitData[2])))
    # else:
    #     client.publish("sensor03", splitData[2])
    #     writelog((" Lumi: " + str(splitData[2])))
 
def writeData(data):
    ser.write(str(data).encode())
