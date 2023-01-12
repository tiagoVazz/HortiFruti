import serial #for serial communication with A9     # python -m pip install pyserial
import time
import pygame #to play prerecorded message          # python -m pip install pygame

import serial.tools.list_ports as port_list
ports = list(port_list.comports())      #Confirm open ports
for p in ports:
    print (p)

def sendcommand(command):
    AT_command = command + "\r"
    ser.write(str(AT_command).encode('ascii'))
    time.sleep(1)
    #print("sent: " + command)
    if ser.inWaiting() > 0:
        echo = ser.readline() #waste the echo
        response_byte = ser.readline()
        response_str = response_byte.decode('ascii')
        #print(response_str)
        return (response_str)
    else:
        print("ERROR at sendcommand")
        return ("ERROR at sendcommand")

def initA9():
    if "OK" in (sendcommand("AT")):  # enable txt reading
        #print("A9 Module Responding")
        print()
    else:
        #print("ERROR: A9 Module not found")
        return "ERROR at init AT"

    if ("OK" in (sendcommand("AT+CMGF=1"))) and ("OK" in (sendcommand("AT+CSMP=17,167,0,0"))):  # enable txt reading
        #print("A9 Module: txt reading enabled")
        print()
    else:
        #print("ERROR: A9 Module not online")
        return "ERROR at init online check"

    return "OK"

def sendSMS(message, number):
    #ser.write(b'AT+CMGS="' + number.encode() + b'"\r')
    #sendcommand("AT+CMGS="+number)
    ser.write(str("AT+CMGS=" + number + "\r").encode('ascii'))
    time.sleep(0.5)
    #ser.write(message.encode() + b"\r")
    #sendcommand(message)
    ser.write(str(message).encode('ascii'))
    time.sleep(0.5)
    ser.write(bytes([26]))
    time.sleep(0.5)
    print ("Message sent")
    time.sleep(2)
    ser.flushInput()

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=5)       #open serial port
print("Established communication with", ser.name)

print(sendcommand("AT"))

initA9()

sendSMS("hello, i'm under the water.", "+351913588051")

ser.close()