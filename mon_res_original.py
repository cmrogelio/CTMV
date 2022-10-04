import cv2
import numpy as np
import distancia_f as di
import calculos_f as ca
import colores_f as col
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import centroide_f as ce

def mon_fin(obj1_x,obj1_y,obj2_x,obj2_y,obj3_x,obj3_y,obj4_x,obj4_y,x2,y2,c,t,take,fin,imagen,conv,rute):
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
     
    # Prints: [8.0, 6.0]
    print "Current size:", fig_size
     
    # Set figure width to 12 and height to 9
    fig_size[0] = 12
    fig_size[1] = 15
    plt.rcParams["figure.figsize"] = fig_size

    
    obj1=[obj1_x,obj1_y];
    obj2=[obj2_x,obj2_y];
    obj3=[obj3_x,obj3_y];
    obj4=[obj4_x,obj4_y];
    if(c>0):
        fig = plt.figure()
        des1 = fig.add_subplot(511)
        vel1 = fig.add_subplot(513)
        acel1 = fig.add_subplot(515)
        des1.grid(b=1,axis='both', color='k')
        vel1.grid(b=1,axis='both', color='k')
        acel1.grid(b=1,axis='both', color='k')
        des1.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displacement (mm)")
        vel1.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
        acel1.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
        file = open(str(rute)+"Monitoreo1_blue.txt","w")
        g1 = PdfPages(str(rute)+'Especimen1_blue.pdf')
        print "obj1_x"+str(obj1[0]);
        print "onj1_y"+str(obj1[1]);
        res= col.to3(fin,imagen)
        final=ce.centroide(res,obj1_x,obj1_y,take,0,0,255)
        final=di.line(final,obj1_x,obj1_y,take,0,0,255)
        d1, td1=ca.dis(obj1_x,obj1_y,take,conv)
        v1=ca.vel(d1,t,take)
        a1=ca.acel(v1,t,take)
        des1.plot(td1, color='b', linewidth=1)
        vel1.plot(v1, color='b', linewidth=1)
        acel1.plot(a1, color='b', linewidth=1)
        g1.savefig()
        g1.close()
        file.write("No.\t position x\t position y\t distance(mm)\t velocity(mm/s)\t aceleration(mm/s^2)\n")
        for n in range(0,take):
            file.write("1\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj1[0][n], obj1[1][n], td1[n],v1[n],a1[n]))
        file.close()
        
    if(c>1):
        fig2 = plt.figure()
        des2 = fig2.add_subplot(511)
        vel2 = fig2.add_subplot(513)
        acel2 = fig2.add_subplot(515)
        des2.grid(b=1,axis='both', color='k')
        vel2.grid(b=1,axis='both', color='k')
        acel2.grid(b=1,axis='both', color='k')
        des2.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displacement (mm)")
        vel2.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
        acel2.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
        file = open(str(rute)+"Monitoreo2_red.txt","w")
        g2 = PdfPages(str(rute)+'Especimen2_red.pdf')
        print "obj2_x"+str(obj2[0]);
        print "onj2_y"+str(obj2[1]);
        final=ce.centroide(final,obj2_x,obj2_y,take,255,0,0)
        final=di.line(final,obj2_x,obj2_y,take,255,0,0)
        d2, td2=ca.dis(obj2_x,obj2_y,take,conv)
        v2=ca.vel(d2,t,take)
        a2=ca.acel(v2,t,take)
        des2.plot(td2, color='b', linewidth=1)
        vel2.plot(v2, color='b', linewidth=1)
        acel2.plot(a2, color='b', linewidth=1)
        g2.savefig()
        g2.close()
        file.write("No.\t position x\t position y\t distance(mm)\t velocity(mm/s)\t aceleration(mm/s^2)\n")
        for n in range(0,take):
            file.write("2\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj2[0][n], obj2[1][n], td2[n],v2[n],a2[n]))
        file.close() 
    if(c>2):
        fig3 = plt.figure()
        des3 = fig3.add_subplot(511)
        vel3 = fig3.add_subplot(513)
        acel3 = fig3.add_subplot(515)
        des3.grid(b=1,axis='both', color='k')
        vel3.grid(b=1,axis='both', color='k')
        acel3.grid(b=1,axis='both', color='k')
        des3.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displacement (mm)")
        vel3.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
        acel3.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
        file = open(str(rute)+"Monitoreo3_green.txt","w")
        g3 = PdfPages(str(rute)+'Especimen3_green.pdf')
        print "obj3_x"+str(obj3[0]);
        print "onj3_y"+str(obj3[1]);
        final=ce.centroide(final,obj3_x,obj3_y,take,0,255,0)
        final=di.line(final,obj3_x,obj3_y,take,0,255,0)
        d3, td3=ca.dis(obj3_x,obj3_y,take,conv)
        v3=ca.vel(d3,t,take)
        a3=ca.acel(v3,t,take)
        des3.plot(td3, color='b', linewidth=1)
        vel3.plot(v3, color='b', linewidth=1)
        acel3.plot(a3, color='b', linewidth=1)
        g3.savefig()
        g3.close()
        file.write("No.\t position x\t position y\t distance(mm)\t velocity(mm/s)\t aceleration(mm/s^2)\n")
        for n in range(0,take):
            file.write("3\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj3[0][n], obj3[1][n], td3[n],v3[n],a3[n]))
        file.close()
    if(c>3):
        fig4 = plt.figure()
        des4 = fig4.add_subplot(511)
        vel4 = fig4.add_subplot(513)
        acel4 = fig4.add_subplot(515)
        des4.grid(b=1,axis='both', color='k')
        vel4.grid(b=1,axis='both', color='k')
        acel4.grid(b=1,axis='both', color='k')
        des4.set(title="Time-Displacement", xlabel="Time (sec)",ylabel="Displacement (mm)")
        vel4.set(title="Time-Speed", xlabel="Time (sec)",ylabel="Rapidity (mm/s)")
        acel4.set(title="Time-Acceleration", xlabel="Time (sec)",ylabel="Acceleration (mm/s^2)")
        file = open(str(rute)+"Monitoreo4_yellow.txt","w")
        g4 = PdfPages(str(rute)+'Especimen4_yellow.pdf')
        print "obj4_x"+str(obj4[0]);
        print "onj4_y"+str(obj4[1]);
        final=ce.centroide(final,obj4_x,obj4_y,take,255,242,0)
        final=di.line(final,obj4_x,obj4_y,take,255,242,0)
        d4, td4=ca.dis(obj4_x,obj4_y,take,conv)
        v4=ca.vel(d4,t,take)
        a4=ca.acel(v4,t,take)
        des4.plot(td4, color='b', linewidth=1)
        vel4.plot(v4, color='b', linewidth=1)
        acel4.plot(a4, color='b', linewidth=1)
        g4.savefig()
        g4.close()
        file.write("No.\t position x\t position y\t distance(mm)\t velocity(mm/s)\t aceleration(mm/s^2)\n")
        for n in range(0,take):
            file.write("3\t %5.3f \t %5.3f \t %5.3f \t\t %5.3f\t\t\t %5.3f\n"%(obj4[0][n], obj4[1][n], td4[n],v4[n],a3[n]))
        file.close()
    #cv2.imshow("res",final)
    cv2.imwrite(str(rute)+"Final_res.png",final)
