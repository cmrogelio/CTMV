from datetime import datetime
import time
from calendar import timegm

def temporizador(Y,M,D,h,m,s):
    utc_time = datetime.strptime(str(Y)+"-"+str(M)+"-"+str(D)+"T"+str(h)+":"+str(m)+":"+str(s)+".000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()

    while 1:
        epoch = datetime(1970,1,1)
        i = datetime.now()
        delta_time = (i - epoch).total_seconds()
        if(delta_time>=epoch_time):
            break
