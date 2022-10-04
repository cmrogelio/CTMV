def comparacion(c,x,y,x2,y2,dif):
    for m in range(0,c):
        difx=abs(x2-x[m]);
        print difx
        if (difx<dif):
            dify=abs(y2-y[m]);
            print dify
            if (dify<dif):
                x2=x[m];
                y2=y[m];
                break;

    return x2, y2
