import cv2
import numpy as np
import time
import mon_loop as ml
import mon_res as mr

obj1_x=[];
obj1_y=[];

obj2_x=[];
obj2_y=[];

obj3_x=[];
obj3_y=[];

init=1
take=0
t=1;
conv=1; #convercion a milimetros
flag=0;
h=0;
x2=[];
y2=[];


while (flag==0):
    for m in range(0,60):
        for k in range(init,60):
            imagen1 = cv2.imread("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Imagenes_Tomadas/"+str(h)+"_"+str(m)+"_"+ str(k)+ "_0.png");
            if imagen1 is not None:
                take+=1
                imagen=np.copy(imagen1)
                cv2.imshow("im",imagen)
                obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,x2,y2,c,fin = ml.mon_cal(imagen,h,m,k,obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,x2,y2)
            else:
                break
        init=0
        if imagen1 is None:
            flag=1
            break
    h+=1;
mr.mon_fin(obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,x2,y2,c,t,take,fin,imagen,conv)
    
cv2.waitKey()
