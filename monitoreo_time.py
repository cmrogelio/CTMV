import cv2
import time
import numpy as np
import funciones as fu
import umbral_f as um
import apertura1_f as ap
import cierre1_f as ci
import cont_cen1_f as co
import centroide_f as ce
import comparacion_f as com
import distancia_f as di
import calculos_f as ca
import colores_f as col
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#///////////////Establecer el tamaño de las graficas

# Get current size
fig_size = plt.rcParams["figure.figsize"]
 
# Prints: [8.0, 6.0]
print "Current size:", fig_size
 
# Set figure width to 12 and height to 9
fig_size[0] = 12
fig_size[1] = 15
plt.rcParams["figure.figsize"] = fig_size

#/////////////Parametros iniciales
t0=time.time()
t=1;
conv=1; #convercion a milimetros
segundos=10;
minutos=0;
horas=0;
take=segundos+minutos*60+horas*3600;#numero de capturas
flag=0;
h=0;

obj1_x=[];
obj1_y=[];

obj2_x=[];
obj2_y=[];

obj3_x=[];
obj3_y=[];

init=1

while (flag==0):
    for m in range(0,60):
        for k in range(init,60):
            if(k>segundos and m>=minutos and h>=horas):
                print "horas="+str(h)+", minutos="+str(m)+", segundos="+ str(k)
                flag=1
                break
            imagen = cv2.imread("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Imagenes_Tomadas/"+str(h)+"_"+str(m)+"_"+ str(k)+ "_0.png");
            if imagen is not None:
                print str(k)+ ".jpg";
                grey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
                uv,bina = cv2.threshold(grey,45,255,cv2.THRESH_BINARY_INV)
                aper=ap.apertura(bina,2)
                cier=ci.cierre(aper,2)
                con,fin, x, y, c=co.cont(cier)
                cv2.imwrite("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Res/"+str(h)+"_"+str(m)+"_"+ str(k)+ "_0.png",con)
                print "x"+str(k)+"= " + str(x)
                print "y"+str(k)+"= " + str(y)                
                if(k==1 and m==0):
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
                    
                else:
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
                break
        init=0
        if(k>segundos and m>=minutos and h>=horas):
            break
        if imagen is None:
            flag=1
            break
    h+=1;

print "take="+str(take)      
obj1=[obj1_x,obj1_y];
obj2=[obj2_x,obj2_y];
obj3=[obj3_x,obj3_y];
if(c>0):
    fig = plt.figure()
    des1 = fig.add_subplot(511)
    vel1 = fig.add_subplot(513)
    acel1 = fig.add_subplot(515)
    des1.grid(b=1,axis='both', color='k')
    vel1.grid(b=1,axis='both', color='k')
    acel1.grid(b=1,axis='both', color='k')
    des1.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displcement (mm)")
    vel1.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
    acel1.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
    file = open("Monitoreo1.txt","w")
    g1 = PdfPages('Especimen1.pdf')
    print "obj1_x"+str(obj1[0]);
    print "onj1_y"+str(obj1[1]);
    res= col.to3(fin,imagen)
    final=ce.centroide(res,obj1_x,obj1_y,take,0,0,255)
    final=di.line(final,obj1_x,obj1_y,take,0,0,255)
    d1, td1=ca.dis(obj1_x,obj1_y,take,conv)
    v1=ca.vel(d1,t,take)
    a1=ca.acel(v1,t,take)
    des1.plot(td1, color='b', linewidth=1)
    vel1.plot(v1, color='b', linewidth=1)
    acel1.plot(a1, color='b', linewidth=1)
    g1.savefig()
    g1.close()
    file.write("No.\t posición x\t posición y\t distancia(mm)\t velocidad(mm/s)\t aceleración(mm/s^2)\n")
    for n in range(0,take):
        file.write("1\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj1[0][n], obj1[1][n], td1[n],v1[n],a1[n]))
    file.close()
    
if(c>1):
    fig2 = plt.figure()
    des2 = fig2.add_subplot(511)
    vel2 = fig2.add_subplot(513)
    acel2 = fig2.add_subplot(515)
    des2.grid(b=1,axis='both', color='k')
    vel2.grid(b=1,axis='both', color='k')
    acel2.grid(b=1,axis='both', color='k')
    des2.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displcement (mm)")
    vel2.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
    acel2.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
    file = open("Monitoreo2.txt","w")
    g2 = PdfPages('Especimen2.pdf')
    print "obj2_x"+str(obj2[0]);
    print "onj2_y"+str(obj2[1]);
    final=ce.centroide(final,obj2_x,obj2_y,take,255,0,0)
    final=di.line(final,obj2_x,obj2_y,take,255,0,0)
    d2, td2=ca.dis(obj2_x,obj2_y,take,conv)
    v2=ca.vel(d2,t,take)
    a2=ca.acel(v2,t,take)
    des2.plot(td2, color='b', linewidth=1)
    vel2.plot(v2, color='b', linewidth=1)
    acel2.plot(a2, color='b', linewidth=1)
    g2.savefig()
    g2.close()
    file.write("No.\t posición x\t posición y\t distancia(mm)\t velocidad(mm/s)\t aceleración(mm/s^2)\n")
    for n in range(0,take):
        file.write("2\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj2[0][n], obj2[1][n], td2[n],v2[n],a2[n]))
    file.close() 
if(c>2):
    fig3 = plt.figure()
    des3 = fig3.add_subplot(511)
    vel3 = fig3.add_subplot(513)
    acel3 = fig3.add_subplot(515)
    des3.grid(b=1,axis='both', color='k')
    vel3.grid(b=1,axis='both', color='k')
    acel3.grid(b=1,axis='both', color='k')
    des3.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displcement (mm)")
    vel3.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
    acel3.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
    file = open("Monitoreo3.txt","w")
    g3 = PdfPages('Especimen3.pdf')
    print "obj3_x"+str(obj3[0]);
    print "onj3_y"+str(obj3[1]);
    final=ce.centroide(final,obj3_x,obj3_y,take,0,255,0)
    final=di.line(final,obj3_x,obj3_y,take,0,255,0)
    d3, td3=ca.dis(obj3_x,obj3_y,take,conv)
    v3=ca.vel(d3,t,take)
    a3=ca.acel(v3,t,take)
    des3.plot(td3, color='b', linewidth=1)
    vel3.plot(v3, color='b', linewidth=1)
    acel3.plot(a3, color='b', linewidth=1)
    g3.savefig()
    g3.close()
    file.write("No.\t posición x\t posición y\t distancia(mm)\t velocidad(mm/s)\t aceleración(mm/s^2)\n")
    for n in range(0,take):
        file.write("3\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj3[0][n], obj3[1][n], td3[n],v3[n],a3[n]))
    file.close() 

cv2.imshow("res",final)
cv2.imwrite("C:/Users/rogelio/Documents/9 Semestre/vision/practicas/Res/final.png",final)

t1=time.time()

print "tiempo="+str(t1-t0)

cv2.waitKey()
