import cv2
import numpy as np
import math

def dis(x,y,cont,conv):
    d=[]
    d.append(0.0)
    td=[]
    td.append(0.0)
    total=0
    for k in range(0,cont-1):
        a=(float(x[k])-float(x[k+1]))
        b=(float(y[k])-float(y[k+1]))
        dis=math.sqrt(a*a+b*b)
        if dis<=1.41:
            dis=0
        else:
            dis=dis/conv
        total=total+dis
        #print "distancia="+str(dis)+", x0="+str(x[k])+", x1="+str(x[k])
        d.append(dis)
        td.append(total)
    print "distancia="+str(td)
    return d, td

def vel(d,t,cont):
    v=[]
    for k in range(0,cont):
        vel=(float(d[k])/t)
        #print "velocidad="+str(vel)
        v.append(vel)
    print "velocidad="+str(v)
    return v

def acel(v,t,cont):
    a=[]
    #a.append(0.0)
    for k in range(0,cont-1):
        b=(float(v[k+1])-float(v[k]))
        acel=b/t
        #print "aceleracion="+str(vel)
        a.append(acel)
    a.append(acel)
    print "aceleracion="+str(a)
    return a
    
    


    
