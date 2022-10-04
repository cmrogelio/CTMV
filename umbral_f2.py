import numpy as np 

def umbral(imagen,um):

    alto, ancho, canales = imagen.shape;
    aux=np.copy(imagen);
    val=um;
    for i in range (0,ancho):
        for j in range (0,alto):
            gris=0.299*imagen[j,i,0]+0.587*imagen[j,i,1]+0.114*imagen[j,i,2]; # pasar a escala de grises
            if gris>val: # es posible generar un rango de valores
                aux2 = 255;
            else:
                aux2 = 0;
            #print "val= " + str(val)+", gris=" + str(gris) +", aux=" + str(aux2)
            aux[j,i,0]=aux2;
            aux[j,i,1]=aux2;
            aux[j,i,2]=aux2;
    return aux
