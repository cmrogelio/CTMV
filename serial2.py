import serial
import cv2

arduinoData= serial.Serial('com4',9600)

def led_on():
    arduinoData.write('1')

def led_off():
    arduinoData.write('0')

t=0
s=0

while(1):
    while(s<100):
        if(s % 10 == 0):
            print str(s)
        s=s+1
    s=0
    if(t==0):
        led_on()
        t=1
    else:
        led_off()
        t=0
    print "keep"

