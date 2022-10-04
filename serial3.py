import serial
import cv2

arduinoData= serial.Serial('com4',9600)

def led_on1():
    arduinoData.write("1000")

def led_on2():
    arduinoData.write("0100")

def led_on3():
    arduinoData.write("0010")

def led_on4():
    arduinoData.write("0001")

def led_off():
    arduinoData.write("0000")

t=0
s=0

while(1):
    while(s<2000):
        if(s % 10 == 0):
            print str(s)
        s=s+1
    s=0
    if(t==0):
        led_on1()
        t=1
    elif(t==1):
        led_on2()
        t=2
    elif(t==2):
        led_on3()
        t=3
    elif(t==3):
        led_on4()
        t=4
    else:
        led_off()
        t=0
    print "keep"

