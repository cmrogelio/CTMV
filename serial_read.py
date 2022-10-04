import serial, time

arduino = serial.Serial('COM17', 9600)
#time.sleep(0.5)
rawString = arduino.readline()
print(rawString)
arduino.write("1001")
#time.sleep(0.5)
rawString = arduino.readline()
if(int(rawString)==1):
    print(rawString)
else:
    print "nop"
    print(rawString)
#time.sleep(0.5)
#rawString = arduino.readline()
#print(rawString)
#arduino.close()

        if(int(rawString)==1):
             print(rawString)
        else:
             print "nop"
             rawString = self.arduinoData.readline()
             print(rawString)
