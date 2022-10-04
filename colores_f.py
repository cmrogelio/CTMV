import numpy as np
import cv2

def to3(img,imagen):
    alto, ancho=img.shape

    copy=np.copy(imagen)

    for i in range(0,alto):
        for j in range(0,ancho):
            copy[i,j,0]=img[i,j]
            copy[i,j,1]=img[i,j]
            copy[i,j,2]=img[i,j]
    return copy
