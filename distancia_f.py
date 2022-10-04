import cv2
import numpy as np

def line(imagen,x,y,cont,r,g,b):

    line=np.copy(imagen);

    for k in range(0,cont-1):
        line=cv2.line(line,(y[k],x[k]),(y[k+1],x[k+1]),(b,g,r),1,8)
    return line
    
            

    
