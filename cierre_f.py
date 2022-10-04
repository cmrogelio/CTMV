import numpy as np
import dilatacion_f as di
import erosion_f as er
import umbral_f as um

def cierre(imagen,n):

    copy=np.copy(imagen);
        
    d  = di.dilatacion(copy,n)
    e  = er.erosion(d,n)
    
    return e
