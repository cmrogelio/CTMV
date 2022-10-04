import numpy as np
import dilatacion1_f as di
import erosion1_f as er
import umbral_f as um

def apertura(imagen,n):

    copy=np.copy(imagen);

    e  = er.erosion(copy,n)
    d  = di.dilatacion(e,n)

    return d
