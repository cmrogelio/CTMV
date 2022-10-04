import cv2
import numpy as np
import funciones as fu
import umbral_f as um
import apertura1_f as ap
import cierre1_f as ci
import cont_cen1_f as co
import centroide_f as ce
import comparacion_f as com

def mon_cal(imagen,h,m,k,obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,obj4_x,obj4_y,x2,y2,rute,dif,area,umb,ape,cie,k2):
    grey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    uv,bina = cv2.threshold(grey,umb,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite(str(rute)+str(h)+"_"+str(m)+"_"+ str(k)+ "_um.png",bina)
    print "aper="+str(ape)
    print "cier="+str(cie)
    aper=ap.apertura(bina,ape)
    cier=ci.cierre(aper,cie)
    cv2.imwrite(str(rute)+str(h)+"_"+str(m)+"_"+ str(k)+ "_ap.png",cier) #comentar
    con,fin, x, y, c=co.cont(cier,area)
    cv2.imwrite(str(rute)+str(h)+"_"+str(m)+"_"+ str(k)+ "_0.png",con) # comentar
    print "x"+str(k)+"= " + str(x)
    print "y"+str(k)+"= " + str(y)                
    if(k==k2 and m==0):
        if(c>0):
            obj1_x.append(x[0]);
            obj1_y.append(y[0]);
        if(c>1):
            obj2_x.append(x[1]);
            obj2_y.append(y[1]);
        if(c>2):
            obj3_x.append(x[2]);
            obj3_y.append(y[2]);
        if(c>3):
            obj4_x.append(x[3]);
            obj4_y.append(y[3]);
        x2=x;
        x2.append(0);
        x2.append(0);
        y2=y;
        y2.append(0);
        y2.append(0);
                        
    else:
        if(c>0):
            x2[0], y2[0]=com.comparacion(c,x,y,x2[0],y2[0],dif)
            obj1_x.append(x2[0]);
            obj1_y.append(y2[0]);
            print "xa"+str(k)+"= " + str(x2[0])
            print "ya"+str(k)+"= " + str(y2[0]) 
        if(c>1):
            x2[1], y2[1]=com.comparacion(c,x,y,x2[1],y2[1],dif)
            obj2_x.append(x2[1]);
            obj2_y.append(y2[1]);
        if(c>2):
            x2[2], y2[2]=com.comparacion(c,x,y,x2[2],y2[2],dif)
            obj3_x.append(x2[2]);
            obj3_y.append(y2[2]);
        if(c>3):
            x2[3], y2[3]=com.comparacion(c,x,y,x2[3],y2[3],dif)
            obj4_x.append(x2[3]);
            obj4_y.append(y2[3]);
            
    return obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,obj4_x,obj4_y,x2,y2,c,fin
