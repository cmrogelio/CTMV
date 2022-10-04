import cv2
import numpy as np

def line(img,x1,y1,x2,y2):
    copy=cv2.copy(img)

    for k in range(x1,x2):
        copy[k,y1,1]=255
        copy[k,y1,0]=0
        copy[k,y1,0]=0
        copy[k,y2,1]=255
        copy[k,y2,0]=0
        copy[k,y2,0]=0

    for k in range(y1,y2):
        copy[x1,k,1]=255
        copy[x1,k,0]=0
        copy[x1,k,2]=0
        copy[x2,k,1]=255
        copy[x2,k,0]=0
        copy[x2,k,2]=0
