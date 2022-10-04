import numpy as np 

def gris(imagen):

    alto, ancho, canales = imagen.shape;
    aux=np.copy(imagen);
    for i in range (0,ancho):
        for j in range (0,alto):
            gris=0.299*imagen[j,i,0]+0.587*imagen[j,i,1]+0.114*imagen[j,i,2]; # pasar a escala de grises
            aux[j,i,0]=gris;
            aux[j,i,1]=gris;
            aux[j,i,2]=gris;
    return aux
