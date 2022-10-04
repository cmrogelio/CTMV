from Tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import monitoreo_f as mon
import tkFileDialog
import mon_loop as ml
import mon_res as mr
import directory as di
from datetime import datetime
from datetime import time as time2
import time
from calendar import timegm
import tkMessageBox

class MyVideoCapture:
     def __init__(self, video_source):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         self.val=0
         if not self.vid.isOpened():
             #raise ValueError("Unable to open video source", video_source)
             self.val=1
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 #return (ret,frame)
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),frame)
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()           

class App:
    def __init__(self, main, window_title):
        self.window = main
        self.window.title(window_title)
        #self.video_source = video_source

        self.window.geometry("1330x640")   #1330x580

        self.r=IntVar()
        self.fps=IntVar()
        self.video=0
        self.now = datetime.now()
        self.rute="C:/vision/"
        self.test_start=0
        self.start_val=0
        self.state=0

        alto=480
        ancho=640
        sep1=70+ancho
        pad=60
        self.capf=0;

        self.umbral=45
        self.aper=2
        self.cier=2

        #self.vid = MyVideoCapture(self.video_source)

        self.canvas=Canvas(main,bd=3,relief="sunken",bg="black",height=alto-10,width=ancho-10)
        self.canvas.grid(row=1,column=0,columnspan=3,rowspan=6,padx=(20,20))
        self.dis_imagen = cv2.imread("logo.png");
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(self.dis_imagen, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        #/////Title
        self.canvas1=Canvas(main,height=100,width=100)
        self.canvas1.grid(row=0,column=0,padx=(20,0))
        self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(cv2.imread("uaq1.png"), cv2.COLOR_BGR2RGB)))
        self.canvas1.create_image(0, 0, image = self.photo1, anchor = NW)

        self.ln=Label(main, text=" Crayﬁsh-Tracking Motion Vision ",anchor='center',font=('Arial',20,'bold'))
        self.ln.grid(row=0,column=3,columnspan=3)

        self.lt=Label(main, text="Universidad Autónoma de Querétaro\nFacultad de Ingeniería",anchor='center',font=('Arial',18,'bold'))
        self.lt.grid(row=0,column=1,sticky=W)
        
        self.canvas2=Canvas(main,height=100,width=100)
        self.canvas2.grid(row=0,column=2,sticky=E)
        self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(cv2.imread("unam.png"), cv2.COLOR_BGR2RGB)))
        self.canvas2.create_image(0, 0, image = self.photo2, anchor = NW)

        #/////////Botones
        self.commands_box=LabelFrame(main,text="Commands")
        self.commands_box.grid(row=1,column=3,rowspan=2,sticky=NW,padx=(0,10))

        self.cb=Frame(self.commands_box)
        self.cb.grid()

        self.start=Button(self.cb,text="Start",width=12,state='disable',command=self.start_b)
        self.start.grid(row=0,sticky=W,pady=5,padx=10)

        self.Set=Button(self.cb,text="Set",width=12,command=self.set_conf)
        self.Set.grid(row=2,sticky=W,pady=5,padx=10)

        self.Open=Button(self.cb,text="Open",width=12,command=self.height)
        self.Open.grid(row=4,sticky=W,pady=5,padx=10)

        self.modify=Button(self.cb,text="Modify",width=12,state='disable',command=self.release)
        self.modify.grid(row=3,sticky=W,pady=5,padx=10)

        self.stop=Button(self.cb,text="Stop",width=12,state='disable',command=self.stop_vid)
        self.stop.grid(row=1,sticky=W,pady=(5,8),padx=10)

        self.About=Button(main,text="About",width=12,command=self.about_w)
        self.About.grid(row=7,column=0)
        
        self.adv_set=Button(main,text="Settings",width=12,command=self.adv_settings)
        self.adv_set.grid(row=7,column=1,sticky=W)

        self.vid_b=Button(main,text="video",width=12,command=self.vid_init)
        self.vid_b.grid(row=7,column=2,sticky=W)

        #/////Estado
        self.status_box=LabelFrame(main,text="Test status")
        self.status_box.grid(row=3,column=3,sticky=NW,padx=(0,10))

        self.sb=Frame(self.status_box)
        self.sb.grid()

        self.ltest=Label(self.sb, text="Test:",anchor='center',font=('Arial',10))
        self.ltest.grid(row=0, sticky=W,pady=(5,0))

        self.lnum=Label(self.sb, text="00",anchor='center',font=('Arial',10))
        self.lnum.grid(row=0,column=1, sticky=W)

        self.ltime=Label(self.sb, text="00:00:00",anchor='center',font=('Arial',10,'bold'))
        self.ltime.grid(row=2,columnspan=2,pady=(2,3))

        self.lrem=Label(self.sb, text="Remaining img:",anchor='center',font=('Arial',10))
        self.lrem.grid(row=1, sticky=W)

        self.lrnum=Label(self.sb, text="00",anchor='center',font=('Arial',10))
        self.lrnum.grid(row=1,column=1, sticky=W)

        #/////////Guardado
        self.save_rute=LabelFrame(main,text="Save rute")
        self.save_rute.grid(row=1,column=4,columnspan=2,sticky=N)

        self.sr=Frame(self.save_rute)
        self.sr.grid()

        self.search=Button(self.sr,text="Search",width=12,state='disable',command=self.search_b)
        self.search.grid(row=2,column=1, pady=(0,2),padx=100,columnspan=2)

        self.dr=Radiobutton(self.sr,text="Default route",variable=self.r, value=1,command=self.save_r) #default route
        self.dr.grid(row=0, sticky=W,pady=(10,2))
        self.dr.select()

        self.cr=Radiobutton(self.sr,text="Choose route",variable=self.r, value=2,command=self.save_r) #choose route
        self.cr.grid(row=1, sticky=W,pady=2)
        self.cr.deselect()
            
        self.crn=Radiobutton(self.sr,text="Choose route and name",variable=self.r, value=3,command=self.save_r) #choose route and name
        self.crn.grid(row=2, sticky=W,pady=(2,15))
        self.crn.deselect()

        self.l1=Label(self.sr, text="The name is generated by the date")
        self.l1.grid(row=1,column=1,columnspan=2)

        self.l15=Label(self.sr, text="File name:")
        self.l15.grid(row=0,column=1)

        self.name_f=StringVar()
        self.e13=Entry(self.sr,textvariable=self.name_f,width=15)
        self.e13.grid(row=0,column=2,sticky=W)
        self.e13.delete(0,END)
        self.e13.insert(0,str(self.now.year)+"-"+str(self.now.month)+"-"+str(self.now.day)+"-"+str(self.now.hour)+"-"+str(self.now.minute));
        self.e13.configure(state='disable')

        #/////////FPS
        self.fps_box=LabelFrame(main,text="FPS")
        self.fps_box.grid(row=2,column=4,columnspan=2,sticky=N)

        self.fb=Frame(self.fps_box)
        self.fb.grid()

        self.l2=Label(self.fb, text="Number of images taken per second")
        self.l2.grid(row=0,sticky=W, pady=5,rowspan=2,padx=60)

        self.fps1=Radiobutton(self.fb,text="1 FPS",variable=self.fps, value=1) #default route
        self.fps1.grid(row=0,column=1,padx=(10,67))
        self.fps1.select()

        self.fps2=Radiobutton(self.fb,text="2 FPS",variable=self.fps, value=2,state='disable') #default route
        self.fps2.grid(column=1,row=1,padx=(10,67))
        self.fps2.deselect()

        #/////////Tiempo de pruebas
        self.Testing_box=LabelFrame(main,text="Testing conditions")
        self.Testing_box.grid(row=3,column=4,columnspan=2,sticky=N)

        self.tb=Frame(self.Testing_box)
        self.tb.grid()

        self.l3=Label(self.tb, text="Number of test to perform")
        self.l3.grid(row=0,sticky=W,pady=2,padx=(70,50))

        self.l4=Label(self.tb, text="Rest time between test")
        self.l4.grid(row=1,sticky=W,pady=2,padx=(70,50))

        self.l5=Label(self.tb, text="Duration of time per test")
        self.l5.grid(row=2,sticky=W,pady=2,padx=(70,50))

        self.test_no=IntVar()
        self.e1=Entry(self.tb,textvariable=self.test_no,width=5)
        self.e1.grid(row=0,column=1,padx=2)
        self.e1.delete(0,END)
        self.e1.insert(0,1)

        self.rest_time=IntVar()
        self.e2=Entry(self.tb,textvariable=self.rest_time,width=5)
        self.e2.grid(row=1,column=1,padx=2)

        self.test_time=IntVar()
        self.e3=Entry(self.tb,textvariable=self.test_time,width=5)
        self.e3.grid(row=2,column=1,padx=2)

        self.hrs1=Label(self.tb, text="Hrs.")
        self.hrs1.grid(row=1,column=2,sticky=W)

        self.hrs2=Label(self.tb, text="Hrs.")
        self.hrs2.grid(row=2,column=2,sticky=W)

        self.rt_min=IntVar()
        self.e4=Entry(self.tb,textvariable=self.rt_min,width=5)
        self.e4.grid(row=1,column=3,padx=2)

        self.tt_min=IntVar()
        self.e5=Entry(self.tb,textvariable=self.tt_min,width=5)
        self.e5.grid(row=2,column=3,padx=2)

        self.min1=Label(self.tb, text="Min.")
        self.min1.grid(row=1,column=4,sticky=W,padx=(0,51))

        self.min2=Label(self.tb, text="Min.")
        self.min2.grid(row=2,column=4,sticky=W,padx=(0,51))

        #//////////Start time
        self.time_box=LabelFrame(main,text="Start time")
        self.time_box.grid(row=4,column=4,columnspan=2,sticky=N)

        self.tbox=Frame(self.time_box)
        self.tbox.grid()

        self.pr=IntVar()
        self.program=Checkbutton(self.tbox,text="Set a start time",variable=self.pr,command=self.st_active)
        self.program.grid(row=0,column=0,columnspan=6,sticky=W)

        self.l6=Label(self.tbox, text="Date")
        self.l6.grid(row=1,sticky=W,padx=100)

        self.l7=Label(self.tbox, text="Set time")
        self.l7.grid(row=3,sticky=W,padx=100)

        self.l8=Label(self.tbox, text="YYYY")
        self.l8.grid(row=2,column=1)

        self.l9=Label(self.tbox, text="MM")
        self.l9.grid(row=2,column=3)

        self.l10=Label(self.tbox, text="DD")
        self.l10.grid(row=2,column=5,padx=(0,77))

        self.s1=Label(self.tbox, text="/")
        self.s1.grid(row=1,column=2)

        self.s2=Label(self.tbox, text="/")
        self.s2.grid(row=1,column=4)

        self.dy=IntVar()
        self.e6=Entry(self.tbox,textvariable=self.dy,width=5)
        self.e6.grid(row=1,column=1)
        self.e6.delete(0,END)
        self.e6.insert(0,str(self.now.year))
        self.e6.configure(state='disable')

        self.dm=IntVar()
        self.e7=Entry(self.tbox,textvariable=self.dm,width=5)
        self.e7.grid(row=1,column=3)
        self.e7.delete(0,END)
        self.e7.insert(0,str(self.now.month))
        self.e7.configure(state='disable')

        self.dd=IntVar()
        self.e8=Entry(self.tbox,textvariable=self.dd,width=5)
        self.e8.grid(row=1,column=5,padx=(0,77))
        self.e8.delete(0,END)
        self.e8.insert(0,str(self.now.day))
        self.e8.configure(state='disable')

        self.l11=Label(self.tbox, text="HH")
        self.l11.grid(row=4,column=1)

        self.l12=Label(self.tbox, text="MM")
        self.l12.grid(row=4,column=3)

        self.l13=Label(self.tbox, text="SS")
        self.l13.grid(row=4,column=5,padx=(0,77))

        self.d1=Label(self.tbox, text=":")
        self.d1.grid(row=3,column=2)

        self.d2=Label(self.tbox, text=":")
        self.d2.grid(row=3,column=4)

        self.th=IntVar()
        self.e9=Entry(self.tbox,textvariable=self.th,width=5)
        self.e9.grid(row=3,column=1)
        self.e9.delete(0,END)
        self.e9.insert(0,str(self.now.hour))
        self.e9.configure(state='disable')

        self.tm=IntVar()
        self.e10=Entry(self.tbox,textvariable=self.tm,width=5)
        self.e10.grid(row=3,column=3)
        self.e10.delete(0,END)
        self.e10.insert(0,str(self.now.minute))
        self.e10.configure(state='disable')

        self.ts=IntVar()
        self.e11=Entry(self.tbox,textvariable=self.ts,width=5,state='disable')
        self.e11.grid(row=3,column=5,padx=(0,77))

        #///////////////Distance
        self.distance_box=LabelFrame(main,text="Distance")
        self.distance_box.grid(row=5,column=4,sticky=N)

        self.db=Frame(self.distance_box)
        self.db.grid()

        self.l14=Label(self.db, text="Height of the camera(40-80 cm)")
        self.l14.grid(row=0,column=0, pady=3,padx=35)

        self.distance=IntVar()
        self.e12=Entry(self.db,textvariable=self.distance,width=5)
        self.e12.grid(row=1,column=0,pady=(2,2))
        self.e12.delete(0,END)
        self.e12.insert(0,68)

        #///////////Process
        self.process_box=LabelFrame(main,text="Process")
        self.process_box.grid(row=5,column=5,sticky=N)

        self.pb=Frame(self.process_box)
        self.pb.grid()

        self.pros=IntVar()
        self.cap=Radiobutton(self.pb,text="Capture",variable=self.pros, value=1) #default route
        self.cap.grid(row=0,column=0,padx=(0,5),sticky=W)
        self.cap.select()

        self.cap_mon=Radiobutton(self.pb,text="Capture and processing",variable=self.pros, value=2) #default route
        self.cap_mon.grid(row=1,column=0,padx=(0,38),sticky=W)
        self.cap_mon.deselect()

        self.delay = 5

        self.cam_con()

        #self.img_loop()

        self.window.mainloop()

    def about_w(self):
         self.a_w=Toplevel(self.window)
         self.a_w.geometry("550x250")
         self.a_w.title("About the software")
        
         self.al1=Label(self.a_w, text="The Software Crayfish-Traking Motion Vision software was develop\nby the student Rogelio Cedeño Moreno from the Engineering Faculty \nof the Autonomous Querétaro University. And it was presented as a \nthesis topic.",justify="left",font=('Arial',12))
         self.al1.grid(row=1,column=0,padx=(4,0),pady=(0,4))

         self.al2=Label(self.a_w, text="The software was designed under the specifications of the department\nof physiology of the National Autonomous Mexico University, in order\nto support their research related with the identification of the \nProcambarus Clarkii physical substrates.",justify="left",font=('Arial',12))
         self.al2.grid(row=2,column=0,padx=(4,0),pady=(0,4))

         self.al4=Label(self.a_w, text="This software is limited to the monitoring of 1 to 4 specimens and in\nthe actual version the specimens must be in individual areas.",justify="left",font=('Arial',12))
         self.al4.grid(row=3,column=0,padx=(0,0),pady=(0,4))

         self.al3=Label(self.a_w, text="About the software...",justify="left",font=('Arial',15))
         self.al3.grid(row=0,column=0,padx=(4,0),pady=(0,4))

    def adv_settings(self):
         di.createFolder(self.rute)
         
         self.a_s=Toplevel(self.window)
         self.a_s.geometry("200x250")
         self.a_s.title("Advance settings")
         
         self.settings_box=LabelFrame(self.a_s,text="Parameters")
         self.settings_box.grid(row=0,column=0, padx=(7,0),pady=(10,10))
         
         self.asb=Frame(self.settings_box)
         self.asb.grid()
         
         self.asl1=Label(self.asb, text="Umbral",justify="left")
         self.asl1.grid(row=0,column=0,padx=(10,0),pady=(10,8),sticky=W)

         self.asl2=Label(self.asb, text="Apertura",justify="left")
         self.asl2.grid(row=1,column=0,padx=(10,0),pady=(0,8),sticky=W)

         self.asl3=Label(self.asb, text="Cierre",justify="left")
         self.asl3.grid(row=2,column=0,padx=(10,0),pady=(0,8),sticky=W)

         self.ase1_v=IntVar()
         self.ase1=Entry(self.asb,textvariable=self.ase1_v,width=13)
         self.ase1.grid(row=0,column=1,padx=(10,5))
         self.ase1.delete(0,END)
         self.ase1.insert(0,45)

         self.ase2_v=IntVar()
         self.ase2=Entry(self.asb,textvariable=self.ase2_v,width=13)
         self.ase2.grid(row=1,column=1,padx=(10,5))
         self.ase2.delete(0,END)
         self.ase2.insert(0,2)
         
         self.ase3_v=IntVar()
         self.ase3=Entry(self.asb,textvariable=self.ase3_v,width=13)
         self.ase3.grid(row=2,column=1,padx=(10,5))
         self.ase3.delete(0,END)
         self.ase3.insert(0,2)

         #/////////

         self.as_set=Button(self.a_s,text="Accept",width=15,command=self.a_s.destroy)
         self.as_set.grid(row=3,column=0,pady=(5,5))

         self.as_cap=Button(self.a_s,text="Capture",width=15,command=self.capture)
         self.as_cap.grid(row=1,column=0,pady=(5,5))

         self.as_an=Button(self.a_s,text="Analize",width=15,command=self.analize)
         self.as_an.grid(row=2,column=0,pady=(5,5))

    def capture(self):
         ret, frame, img = self.vid.get_frame()
         self.start_val=1
         if(ret):
              cv2.imwrite("C:/vision/test/0_0_1_0.png",img)
              self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
              self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
         
    def analize(self):
         self.direc= "C:/vision/test"
         self.rute=str(self.direc)+"/Processed_img/"
         self.rute_res=str(self.direc)+"/Res/"
         di.createFolder(self.rute)
         di.createFolder(self.rute_res)
         self.start_val=0

         self.umbral=self.ase1_v.get()
         self.aper=self.ase2_v.get()
         self.cier=self.ase3_v.get()

         self.capf=1;
         
         self.img_loop()
         self.obj1_x=[];
         self.obj1_y=[];

         self.obj2_x=[];
         self.obj2_y=[];

         self.obj3_x=[];
         self.obj3_y=[];

         init=1
         self.take=0
         self.t=1;
         d=68
         self.conv=(d+567)/(0.89*d*10); #convercion a milimetros
         self.dif=self.conv*38.5921
         self.area=self.conv*953.07
         self.im_rem=0

         self.x2=[];
         self.y2=[];
         self.thoras=0
         self.tminutos=0
         self.tseg=0
         self.dis_imagen = cv2.imread(str(self.direc)+"/0_0_1_0.png");
         self.test()
         
    def release(self):
         if self.state ==1:
              self.vid.vid.release()
         self.cam_con()
        
    def cam_con(self):
                 #/////////////CAMARA
        self.Set.configure(state='disable')
        self.start.configure(state='disable')
        self.modify.configure(state='disable')
        self.dr.configure(state='disable')
        self.cr.configure(state='disable')
        self.crn.configure(state='disable')
        self.fps1.configure(state='disable')
        self.fps2.configure(state='disable')
        self.program.configure(state='disable')
        self.e1.configure(state='disable')
        self.e2.configure(state='disable')
        self.e3.configure(state='disable')
        self.e4.configure(state='disable')
        self.e5.configure(state='disable')
        self.e6.configure(state='disable')
        self.e7.configure(state='disable')
        self.e8.configure(state='disable')
        self.e9.configure(state='disable')
        self.e10.configure(state='disable')
        self.e11.configure(state='disable')
        self.e12.configure(state='disable')
        self.e13.configure(state='disable')
        self.cap.configure(state='disable')
        self.cap_mon.configure(state='disable')
        self.vid_b.configure(state='disable')
        self.adv_set.configure(state='disable')
        
        self.m_cam=Toplevel(self.window)
        self.m_cam.geometry("250x180")
        self.m_cam.title("Camera selection")
        
        self.cl1=Label(self.m_cam, text="Camera selection",anchor='center',font=('Arial',15,'bold'))
        self.cl1.grid(row=0,column=0,columnspan=2,padx=(4,0),pady=(0,4))

        self.vs=IntVar()
        self.ce1=Entry(self.m_cam,textvariable=self.vs,width=13)
        self.ce1.grid(row=1,column=0,padx=(10,5),pady=(0,4))
        self.ce1.delete(0,END)
        self.ce1.insert(0,0)

        self.cset=Button(self.m_cam,text="Select",width=12,command=self.button)
        self.cset.grid(row=1,column=1)
        self.cl2=Label(self.m_cam, text="Note: In this program you must \n first select the camera with \n which the program will be \n working, for this you must \n select the number assigned to \n the camera by the computer",justify='center')
        self.cl2.grid(row=2,column=0,columnspan=2,sticky=W,padx=(7,0),pady=(4,0))
        #////////////////

    def button(self):
         self.state=1
         self.vid = MyVideoCapture(self.vs.get())
         if(self.vid.val==1):
              self.cl2.configure(text="Unable to open video source",font=('Arial',10,'bold'),fg='red')
              raise ValueError("Unable to open video source")
         self.m_cam.destroy()
         self.mod_conf()

    def save_r(self):
        a=self.r.get()
        if(a==1):
            self.search.configure(state='disable')
            self.e13.configure(state='disable')
        if(a==2):
            self.search.configure(state='normal')
            self.e13.configure(state='disable')
        if(a==3):
            self.search.configure(state='normal')
            self.e13.configure(state='normal')

    def stop_vid(self):
         self.video=1;
         self.start_val=1
         self.ltime.configure(text="00:00:00")
         self.lrnum.configure(text="00")
         self.lnum.configure(text="00")
         self.stop.configure(state='disable')
         self.Open.configure(state='normal')
         self.release()
            
    def set_conf(self):
        self.Set.configure(state='disable')
        self.start.configure(state='normal')
        self.modify.configure(state='normal')
        self.search.configure(state='disable')
        self.dr.configure(state='disable')
        self.cr.configure(state='disable')
        self.crn.configure(state='disable')
        self.fps1.configure(state='disable')
        self.fps2.configure(state='disable')
        self.program.configure(state='disable')
        self.e1.configure(state='disable')
        self.e2.configure(state='disable')
        self.e3.configure(state='disable')
        self.e4.configure(state='disable')
        self.e5.configure(state='disable')
        self.e6.configure(state='disable')
        self.e7.configure(state='disable')
        self.e8.configure(state='disable')
        self.e9.configure(state='disable')
        self.e10.configure(state='disable')
        self.e11.configure(state='disable')
        self.e12.configure(state='disable')
        self.e13.configure(state='disable')
        self.cap.configure(state='disable')
        self.cap_mon.configure(state='disable')
        

    def mod_conf(self):
        self.Set.configure(state='normal')
        self.start.configure(state='disable')
        self.modify.configure(state='disable')
        self.dr.configure(state='normal')
        self.cr.configure(state='normal')
        self.crn.configure(state='normal')
        self.fps1.configure(state='normal')
        #self.fps2.configure(state='normal')
        self.program.configure(state='normal')
        self.e1.configure(state='normal')
        self.e2.configure(state='normal')
        self.e3.configure(state='normal')
        self.e4.configure(state='normal')
        self.e5.configure(state='normal')
        self.e12.configure(state='normal')
        self.cap.configure(state='normal')
        self.cap_mon.configure(state='normal')
        self.vid_b.configure(state='normal')
        self.adv_set.configure(state='normal')
        self.st_active()
        self.save_r()

    def st_active(self):
        a=self.pr.get()
        if(a==1):
            self.e6.configure(state='normal')
            self.e7.configure(state='normal')
            self.e8.configure(state='normal')
            self.e9.configure(state='normal')
            self.e10.configure(state='normal')
            self.e11.configure(state='normal')
        else:
            self.e6.configure(state='disable')
            self.e7.configure(state='disable')
            self.e8.configure(state='disable')
            self.e9.configure(state='disable')
            self.e10.configure(state='disable')
            self.e11.configure(state='disable')

    def vid_init(self):
         self.start_val=2
         self.vid_button()

    def vid_button(self):
         if(self.start_val==2):
              ret, frame, img = self.vid.get_frame()
              if ret:
                   self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                   self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
                   self.window.after(10, self.vid_button)

    def start_b(self):
         b=self.pr.get()
         self.now = datetime.now()
         self.start_val=1
         self.video=0
         self.start.configure(state='disable')
         self.stop.configure(state='normal')
         self.Open.configure(state='disable')
         self.modify.configure(state='disable')
         self.adv_set.configure(state='disable')
         self.vid_b.configure(state='disable')
         

         a=self.r.get()
         if(a==1):
              self.rute="C:/vision/"+str(self.now.year)+"-"+str(self.now.month)+"-"+str(self.now.day)+"-"+str(self.now.hour)+"-"+str(self.now.minute)+"/"
         elif(a==2):
              self.rute=str(self.rute)+"/"+str(self.now.year)+"-"+str(self.now.month)+"-"+str(self.now.day)+"-"+str(self.now.hour)+"-"+str(self.now.minute)+"/"
         elif(a==3):
              self.rute=str(self.rute)+"/"+str(self.name_f.get())+"/"
         di.createFolder(self.rute)
         for p in range(1,self.test_no.get()+1):
              di.createFolder(self.rute+"/Prueba "+str(p)+"/Img/Processed_img/")
              di.createFolder(self.rute+"/Prueba "+str(p)+"/Img/Res/")
              di.createFolder(self.rute+"/Prueba "+str(p)+"/Img/")
         print "carpetas"+self.rute
         
         h=self.test_time.get();
         m=self.tt_min.get();
         s=0;
         ms=0;

         self.time=s+(m*60)+(h*3600);

         hr=self.rest_time.get()
         mr=self.rt_min.get()
         self.rtime=(mr*60)+(hr*3600);


         self.seg=0;
         self.minutos=0;
         self.horas=0;
         self.prueba=1;
         #///////// calculos
         self.obj1_x=[];
         self.obj1_y=[];

         self.obj2_x=[];
         self.obj2_y=[];

         self.obj3_x=[];
         self.obj3_y=[];

         self.obj4_x=[];
         self.obj4_y=[];

         init=1
         self.take=0
         self.t=1;
         d=self.distance.get()
         self.conv=(d+567)/(0.89*d*10); #convercion a milimetros
         self.dif=self.conv*38.5921
         self.area=self.conv*953.07

         self.x2=[];
         self.y2=[];
         self.thoras=0
         self.tminutos=0
         self.tseg=0
         print "calculos"
        #///////////////////

         Y=self.dy.get()
         M=self.dm.get()
         D=self.dd.get()
         h=self.th.get()
         m=self.tm.get()
         s=self.ts.get()
         self.utc_time = datetime.strptime(str(Y)+"-"+str(M)+"-"+str(D)+"T"+str(h)+":"+str(m)+":"+str(s)+".000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
         self.epoch = datetime(1970,1,1)
         self.epoch_t = (self.utc_time - self.epoch).total_seconds()
         
         self.temp()
         
         
    def temp(self):
         print "temp"
         i = datetime.now()
         fps=self.fps.get()
         delta_time = (i - self.epoch).total_seconds()
         if(delta_time>=self.epoch_t):
              i = datetime.now()
              alfa = (i - self.epoch).total_seconds()
              self.comp=alfa+fps
              self.fin=alfa+self.time
              self.im_rem=self.time
              self.lrnum.configure(text=str(self.im_rem))
              self.lnum.configure(text='1')
              print "inicio"
              self.update()
         else:
              self.ltime.configure(text='Waiting')
              self.window.after(2000, self.temp)

         
    def update(self):
           # Get a frame from the video source
        if self.video!=1:
             print "update"
             ret, frame, img = self.vid.get_frame()
             i = datetime.now()
             delta_time = (i - self.epoch).total_seconds()

             if(delta_time>=self.comp):
                 self.comp+=1
                 if(self.seg+1==60):
                    self.seg=0
                    self.minutos+=1
                 else:
                    self.seg+=1
                 if(self.minutos==60):
                    self.minutos=0
                    self.horas+=1
                 cv2.imwrite(self.rute+"/Prueba "+str(self.prueba)+"/Img/"+str(self.horas)+"_"+str(self.minutos)+"_"+ str(self.seg)+ "_0.png",img)
                 #print "save"
                 d=time2(self.horas,self.minutos,self.seg)
                 self.ltime.configure(text=str(d))
                 self.im_rem-=1
                 self.lrnum.configure(text=str(self.im_rem))
                 print str(delta_time)
             if(delta_time>=self.fin):
                 i = datetime.now()
                 self.delta_time = (i - self.epoch).total_seconds()
                 self.epoch_time=self.delta_time+self.rtime
                 self.rest()
                 #print "okey"
             elif ret:
                 self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                 self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
                 self.window.after(self.delay, self.update)
        else:
             self.video=0
             #print self.video
             
    def rest(self):
         if(self.prueba<self.test_no.get()):
              i = datetime.now()
              self.delta_time = (i - self.epoch).total_seconds()
              if(self.delta_time>=self.epoch_time):
                   self.new_test()
              else:
                   self.ltime.configure(text='Resting')
                   #time.sleep(2)
                   self.window.after(2000, self.rest)
         else:
               self.new_test()
         
    def new_test(self):
         self.ltime.configure(text="00:00:00")
         if(self.prueba<self.test_no.get()):
              self.prueba+=1
              
              fps=self.fps.get()

              self.seg=0;
              self.minutos=0;
              self.horas=0;

              self.im_rem=self.time
              self.lrnum.configure(text=str(self.im_rem))
              i = datetime.now()
              alfa = (i - self.epoch).total_seconds()
              self.comp=alfa+fps
              self.fin=alfa+self.time
              self.lnum.configure(text=str(self.prueba))
              self.update()
         else:
              if(self.pros.get()==2):
                   self.vid.vid.release()
                   self.prueba=0
                   self.start_val=0
                   self.video=0
                   self.rute1=self.rute
                   self.mon_cap()
              else:
                   tkMessageBox.showinfo( "Test", "Test finished!!!");
                   self.stop_vid();

    def mon_cap(self):
         if(self.prueba<self.test_no.get()):
              self.test_start=1
              self.prueba+=1
              self.lnum.configure(text='1')
              self.thoras=0
              self.tminutos=0
              self.tseg=0
              self.direc=self.rute1+"/Prueba "+str(self.prueba)+"/Img"
              self.rute=str(self.direc)+"/Processed_img/"
              self.rute_res=str(self.direc)+"/Res/"
              self.img_loop()
              self.cont_img()
         else:
              tkMessageBox.showinfo( "Test", "Test finished!!!");
              self.cam_con()
              self.ltime.configure(text="00:00:00")
              self.lrnum.configure(text="00")
              self.lnum.configure(text="00")
              self.start_val=0
         
         
    def Set_img(self,imagen):
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imagen))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)


    def search_b(self):
         self.rute= tkFileDialog.askdirectory()

    def height(self):
        self.start.configure(state='disable')
        self.stop.configure(state='normal')
        self.Set.configure(state='disable')
        self.modify.configure(state='disable')
        self.Open.configure(state='disable')
        
        self.m_height=Toplevel(self.window)
        self.m_height.geometry("250x130")
        self.m_height.title("Capture height")
        
        self.hl1=Label(self.m_height, text="Height selection",anchor='center',font=('Arial',15,'bold'))
        self.hl1.grid(row=0,column=0,columnspan=2,padx=(4,0),pady=(0,4))

        self.hdistance=IntVar()
        self.he1=Entry(self.m_height,textvariable=self.hdistance,width=13)
        self.he1.grid(row=1,column=0,padx=(10,5),pady=(0,4))
        self.he1.delete(0,END)
        self.he1.insert(0,68)

        self.hset=Button(self.m_height,text="Select",width=12,command=self.directory)
        self.hset.grid(row=1,column=1)
        self.hl2=Label(self.m_height, text="Note: To process a previous test,\n it is needed to know the height\n with which the test was taken",justify='center')
        self.hl2.grid(row=2,column=0,columnspan=2,sticky=W,padx=(7,0),pady=(4,0))

        
    def directory(self):
        print "analize"
        self.video=0
        self.start_val=0
        self.dis_imagen = cv2.imread("logo.png");
        self.set_conf()
        self.start.configure(state='disable')
        self.modify.configure(state='disable')
        self.adv_set.configure(state='disable')
        self.vid_b.configure(state='disable')
        self.m_height.destroy()
        self.direc= tkFileDialog.askdirectory()
        self.rute=str(self.direc)+"/Processed_img/"
        self.rute_res=str(self.direc)+"/Res/"
        di.createFolder(self.rute)
        di.createFolder(self.rute_res)
        self.img_loop()
        self.obj1_x=[];
        self.obj1_y=[];

        self.obj2_x=[];
        self.obj2_y=[];

        self.obj3_x=[];
        self.obj3_y=[];

        self.obj4_x=[];
        self.obj4_y=[];

        init=1
        self.take=0
        self.t=1;
        d=self.hdistance.get()
        self.conv=(d+567)/(0.89*d*10); #convercion a milimetros
        self.dif=self.conv*38.5921
        self.area=self.conv*953.07

        self.x2=[];
        self.y2=[];
        self.thoras=0
        self.tminutos=0
        self.tseg=0
        self.dis_imagen = cv2.imread(str(self.direc)+"/0_0_1_0.png");
        self.cont_img()

    def cont_img(self):
        print "cont"
        self.im_rem=0
        while 1:
             if(self.tseg+1==60):
                 self.tseg=0
                 self.tminutos+=1
             else:
                 self.tseg+=1
             if(self.tminutos==60):
                 self.tminutos=0
                 self.thoras+=1
             imagen1 = cv2.imread(str(self.direc)+"/"+str(self.thoras)+"_"+str(self.tminutos)+"_"+ str(self.tseg)+ "_0.png");
             if imagen1 is not None:
                  self.im_rem+=1
             else:
                  break
        self.lrnum.configure(text=str(self.im_rem))
        self.thoras=0
        self.tminutos=0
        self.tseg=0
        print "test"
        self.test()
        
    def test(self):
        print "test start"
        if self.video!=1:
             if(self.tseg+1==60):
                 self.tseg=0
                 self.tminutos+=1
             else:
                 self.tseg+=1
             if(self.tminutos==60):
                 self.tminutos=0
                 self.thoras+=1
             imagen1 = cv2.imread(str(self.direc)+"/"+str(self.thoras)+"_"+str(self.tminutos)+"_"+ str(self.tseg)+ "_0.png");
             if imagen1 is not None:
                  d=time2(self.thoras,self.tminutos,self.tseg)
                  self.ltime.configure(text=str(d))
                  self.im_rem-=1
                  self.lrnum.configure(text=str(self.im_rem))
                  self.take+=1
                  imagen=np.copy(imagen1)
                  self.dis_imagen=imagen
                  self.obj1_x,self.obj1_y,self.obj2_x,self.obj2_y,self.obj3_x,self.obj3_y,self.obj4_x,self.obj4_y,self.x2,self.y2,self.c,self.fin = ml.mon_cal(imagen,self.thoras,self.tminutos,self.tseg,self.obj1_x,self.obj1_y,self.obj2_x,self.obj2_y,self.obj3_x,self.obj3_y,self.obj4_x,self.obj4_y,self.x2,self.y2,self.rute,self.dif,self.area,self.umbral,self.aper,self.cier)

                  if(self.capf==1):
                       imagen1 = cv2.imread(str(self.rute)+"/"+str(self.thoras)+"_"+str(self.tminutos)+"_"+ str(self.tseg)+ "_0.png");
                       self.dis_imagen=imagen1
                       self.start_val=1
                       
                  self.window.after(1000, self.test)
                  #print str(self.prueba)+": "+ str(self.thoras)+"_"+str(self.tminutos)+"_"+ str(self.tseg)+ "_0"
             elif (self.capf==0):
                  di.createFolder(self.rute_res)
                  mr.mon_fin(self.obj1_x,self.obj1_y,self.obj2_x,self.obj2_y,self.obj3_x,self.obj3_y,self.obj4_x,self.obj4_y,self.x2,self.y2,self.c,self.t,self.take,self.fin,self.dis_imagen,self.conv,self.rute_res)
                  self.ltime.configure(text="00:00:00")
                  self.lrnum.configure(text="00")
                  if(self.test_start==1):
                       self.mon_cap()
                  else:
                       tkMessageBox.showinfo( "Test", "Test finished!!!");
                       self.release()
                       self.start_val=1
                       self.Open.configure(state='normal')
                       self.stop.configure(state='disable')
             else:
                  self.capf=0
             
    def img_loop(self):
        #cv2.imshow("video",self.timagen)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv2.cvtColor(self.dis_imagen, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        if(self.start_val==0):
             #print "display"
             self.window.after(self.delay, self.img_loop)

#Cam(Tk(), "Camera")
App(Tk(), "Crayﬁsh-Tracking Motion Vision ver.2.1.3")

