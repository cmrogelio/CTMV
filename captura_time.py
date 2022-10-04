from datetime import datetime
import time
from calendar import timegm
import cv2
import numpy as np

vc= cv2.VideoCapture(2)

h=0;
m=1;
s=0;
ms=0;

fps=1

time=s+(m*60)+(h*3600);


seg=0;
minutos=0;
horas=0;
epoch = datetime(1970,1,1)
i = datetime.now()
alfa = (i - epoch).total_seconds()

comp=alfa+fps
fin=alfa+time;
uno, dos = vc.read()

while 1:
    cv2.imshow("video",dos)
    uno, dos = vc.read()
    epoch = datetime(1970,1,1)
    i = datetime.now()
    delta_time = (i - epoch).total_seconds()
    #print "almost"
    
    if(delta_time>=comp):
        comp+=1
        if(seg+1==60):
            seg=0
            minutos+=1
        else:
            seg+=1
        if(minutos==60):
            minutos=0
            horas+=1
        cv2.imwrite("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/capturas/"+str(horas)+"_"+str(minutos)+"_"+ str(seg)+ "_0.png",dos)
        print str(delta_time)
    if(delta_time>=fin):
        break
    if (cv2.waitKey(27)>=0):
        break

cv2.destroyWindow("video")
vc.release()
print "alfa="+str(alfa)+", fin="+str(fin)
