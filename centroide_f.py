import cv2
import numpy as np

def centroide(imagen,x,y,cont,r,g,b):
    cir=np.copy(imagen);

    for k in range(0,cont):
        """"
        for m in range(x[k]-2,x[k]+3):
            for n in range(y[k]-2,y[k]+3):
                cir[m,n,0] = b;
                cir[m,n,1] = g;
                cir[m,n,2] = r;
        """
        cir=cv2.circle(cir,(y[k],x[k]),1,(b,g,r),2,8)
        #print "x="+str(x[k])+", y="+str(y[k])
    return cir
    
            

    
