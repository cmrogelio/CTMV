import numpy as np

def cont(imagen):

    alto, ancho, canales = imagen.shape;
    umbral=np.copy(imagen);

    for i in range(0, alto):
        for j in range(0, ancho):
            gris=0.299*imagen[i,j,0]+0.587*imagen[i,j,1]+0.114*imagen[i,j,2]
            if gris>200:
                umbral[i,j,0] = 255;
                umbral[i,j,1] = 255;
                umbral[i,j,2] = 255;
            else:
                umbral[i,j,0] = 0;
                umbral[i,j,1] = 0;
                umbral[i,j,2] = 0;

    fifo=[]
    cont=0
    aux=np.copy(umbral)
    aux2=np.copy(umbral)
    b=0

    for i in range(0,alto):
        for j in range(0,ancho):
            if aux[i,j,0]!= 0:
                cont=cont+1
                fifo.append([i,j])
                aux[i,j,0]=0
                aux2[i,j,0]=10*cont;
                while(fifo):
                    a=fifo.pop(0)
                    for m in range(a[0]-1,a[0]+2):
                        for n in range(a[1]-1,a[1]+2):
                            
                            ###para definir los contornos
                            if umbral[m,n,0]==0:
                                b=1
                            ####
                            
                            if aux[m,n,0]!= 0:
                                fifo.append([m,n])
                                aux[m,n,0]=0;
                                aux2[m,n,0]=255;
                    
                    ### elimina el relleno
                    if b==0:
                        aux2[a[0],a[1],0]=0
                    b=0
                    ###
                    
    aux2[:,:,1]=aux2[:,:,0]
    aux2[:,:,2]=aux2[:,:,0]
    return cont
    
