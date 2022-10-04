import cv2
import time
import numpy as np
import funciones as fu
import umbral_f as um
import apertura_f as ap
import cierre_f as ci
import cont_cen_f as co
import centroide_f as ce
import comparacion_f as com
import distancia_f as di
import calculos_f as ca

t0=time.time()

#cv2.namedWindow("video")
vc= cv2.VideoCapture(2)

take=2;#numero de capturas

cont=take+1;
"""
#video continuo
while True:
    uno, dos = vc.read()
    cv2.imshow("video",dos)
    if (cv2.waitKey(27)>=0):  #27-> representa la tecla enter
        imagen=np.copy(dos)
        cv2.imwrite("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/prueba/"+ str(cont)+ ".jpg",imagen)
        cont+=1;
    if (cont>take):
        del (vc)
        break;
"""
obj1_x=[];
obj1_y=[];

obj2_x=[];
obj2_y=[];

obj3_x=[];
obj3_y=[];


for k in range(1,cont):
    imagen = cv2.imread("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Imagenes_Tomadas/0_0_"+ str(k)+ "_0.png");
    print str(k)+ ".jpg";
    grey=fu.gris(imagen)
    bina=um.umbral(grey,55)
    aper=ap.apertura(bina,2)
    cier=ci.cierre(aper,3)
    con, x, y, c=co.cont(cier)
    #cv2.imshow("con"+str(k),con)
    cv2.imwrite("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Res/"+str(k)+".png",con)
    print "x"+str(k)+"= " + str(x)
    print "y"+str(k)+"= " + str(y)
    if(k>1):
        if(c>0):
            x2[0], y2[0]=com.comparacion(c,x,y,x2[0],y2[0])
            obj1_x.append(x2[0]);
            obj1_y.append(y2[0]);
        if(c>1):
            x2[1], y2[1]=com.comparacion(c,x,y,x2[1],y2[1])
            obj2_x.append(x2[1]);
            obj2_y.append(y2[1]);
        if(c>2):
            x2[2], y2[2]=com.comparacion(c,x,y,x2[2],y2[2])
            obj3_x.append(x2[2]);
            obj3_y.append(y2[2]);

        
    else:
        if(c>0):
            obj1_x.append(x[0]);
            obj1_y.append(y[0]);
        if(c>1):
            obj2_x.append(x[1]);
            obj2_y.append(y[1]);
        if(c>2):
            obj3_x.append(x[2]);
            obj3_y.append(y[2]);
        x2=x;
        x2.append(0);
        x2.append(0);
        y2=y;
        y2.append(0);
        y2.append(0);
obj1=[obj1_x,obj1_y];
obj2=[obj2_x,obj2_y];
obj3=[obj3_x,obj3_y];
if(c>0):
    file = open("Monitoreo1.txt","w")
    print "obj1_x"+str(obj1[0]);
    print "onj1_y"+str(obj1[1]);
    final=ce.centroide(con,obj1_x,obj1_y,take,0,0,255)
    final=di.line(final,obj1_x,obj1_y,take,0,0,255)
    d1=ca.var(obj1_x,obj1_y,take)
    for n in range(0,take):
        file.write("1\t"+str(obj1[0][n])+"\t"+str(obj1[1][n])+"\t"+str(d1[n])+"\n")
    file.close() 
if(c>1):
    file = open("Monitoreo2.txt","w")
    print "obj2_x"+str(obj2[0]);
    print "onj2_y"+str(obj2[1]);
    final=ce.centroide(final,obj2_x,obj2_y,take,255,0,0)
    final=di.line(final,obj2_x,obj2_y,take,255,0,0)
    d2=ca.var(obj2_x,obj2_y,take)
    for n in range(0,take):
        file.write("2\t"+str(obj2[0][n])+"\t"+str(obj2[1][n])+"\t"+str(d2[n])+"\n")
    file.close() 
if(c>2):
    file = open("Monitoreo3.txt","w")
    print "obj3_x"+str(obj3[0]);
    print "onj3_y"+str(obj3[1]);
    final=ce.centroide(final,obj3_x,obj3_y,take,0,255,0)
    final=di.line(final,obj3_x,obj3_y,take,0,255,0)
    d3=ca.var(obj3_x,obj3_y,take)
    for n in range(0,take):
        file.write("3\t"+str(obj3[0][n])+"\t"+str(obj3[1][n])+"\t"+str(d3[n])+"\n")
    file.close() 

cv2.imshow("res",final)
t1=time.time()
print "tiempo="+str(t1-t0)
cv2.waitKey()
