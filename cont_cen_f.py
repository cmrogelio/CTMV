import cv2
import numpy as np
import centroide_f as ce

def cont(imagen):

    alto, ancho, canales = imagen.shape;
    print "alto= " + str(alto) + "ancho" + str(ancho)
    umbral=np.copy(imagen);

    fifo=[]
    cont=0
    aux=np.copy(umbral)
    aux2=np.copy(umbral)
    b=0
    mt=0;
    nt=0;
    t=0;
    x=[];
    y=[];

    for i in range(1,alto-1):
        for j in range(1,ancho-1):
            if aux[i,j,0]!= 0:
                cont=cont+1
                fifo.append([i,j])
                aux[i,j,0]=0
                aux2[i,j,0]=10*cont;
                while(fifo):
                    a=fifo.pop(0)
                    for m in range(a[0]-1,a[0]+2):
                        for n in range(a[1]-1,a[1]+2):
                            if m<alto and n<ancho:
                                if aux[m,n,0]!= 0 :
                                    fifo.append([m,n])
                                    aux[m,n,0]=0;
                                    mt+=m;
                                    nt+=n;
                                    t+=1;
                                    aux2[m,n,0]=40+20*cont;
                x.append(mt/t);
                y.append(nt/t);
                mt=0;
                nt=0;
                t=0;
                    
    aux2[:,:,1]=aux2[:,:,0]
    aux2[:,:,2]=aux2[:,:,0]

    #aux3=ce.centroide(aux2,x,y,cont,255,255,255);
    print "contador= " + str(cont)
    return aux2, x, y, cont
    
