import numpy as np 

def erosion(imagen,n):

    alto, ancho, canales = imagen.shape;
    copy=np.copy(imagen);
    umbral=np.copy(copy);
    
    for i in range(0, alto):
        for j in range(0, ancho):
            gris=0.299*copy[i,j,0]+0.587*copy[i,j,1]+0.114*copy[i,j,2]
            if gris<200:
                umbral[i,j,0] = 255;
                umbral[i,j,1] = 255;
                umbral[i,j,2] = 255;
            else:
                umbral[i,j,0] = 0;
                umbral[i,j,1] = 0;
                umbral[i,j,2] = 0;

    for k in range(1,n):

        aux=np.copy(umbral)
        
        for i in range(1, alto):
            for j in range(1, ancho):
                if umbral[i,j,0]>umbral[i-1,j,0]:
                    aux[i-1,j,0]=umbral[i,j,0];
                    aux[i-1,j,1]=umbral[i,j,1];
                    aux[i-1,j,2]=umbral[i,j,2];

        aux2=np.copy(aux)

        for i in range(1, alto):
            for j in range(1, ancho):
                if aux[i,j,0]>aux[i,j-1,0]:
                    aux2[i,j-1,0]=aux[i,j,0];
                    aux2[i,j-1,1]=aux[i,j,1];
                    aux2[i,j-1,2]=aux[i,j,2];

        aux3=np.copy(aux2)

        for i in range(1, alto-1):
            for j in range(1, ancho-1):
                if aux2[i,j,0]>aux2[i+1,j,0]:
                    aux3[i+1,j,0]=aux2[i,j,0];
                    aux3[i+1,j,1]=aux2[i,j,1];
                    aux3[i+1,j,2]=aux2[i,j,2];

        aux4=np.copy(aux3)

        for i in range(1, alto-1):
            for j in range(1, ancho-1):
                if aux3[i,j,0]>aux3[i,j+1,0]:
                    aux4[i,j+1,0]=aux3[i,j,0];
                    aux4[i,j+1,1]=aux3[i,j,1];
                    aux4[i,j+1,2]=aux3[i,j,2];
        umbral=np.copy(aux4)

    aux5=np.copy(aux4)
    for i in range(0, alto):
        for j in range(0, ancho):
            if aux4[i,j,0]<200:
                aux5[i,j,0] = 255;
                aux5[i,j,1] = 255;
                aux5[i,j,2] = 255;
            else:
                aux5[i,j,0] = 0;
                aux5[i,j,1] = 0;
                aux5[i,j,2] = 0;

        
    return aux5
