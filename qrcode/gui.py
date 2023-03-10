import tkinter as tk
from PIL import Image, ImageTk
import vlc
import numpy
from aruco_read import aruco

class gui(object):
    def __init__(self):
        self.cameraStatus = False
        self.root = tk.Tk()
        self.root.title("Assistive Robot App")
        self.root.geometry("480x320")
        self.root.iconbitmap("logo.ico")
        self.root.resizable(False, False)

        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.createFrame()
        self.InitButton()
    
    def InitButton(self):
        self.openVidButton = tk.Button(self.buttonFrame, text="Open Video", command=lambda : self.showVideo("video.mp4"))
        self.openCamButton = tk.Button(self.buttonFrame, text="Open Camera", command=self.showCam)        
        self.closeButton = tk.Button(self.buttonFrame, text="Close", command=self.destruct)
        
        # self.pauseButton = tk.Button(self.buttonFrame, text="Pause", command=self.OnPause)
        self.btnText = tk.StringVar()
        self.playpauseButton = tk.Button(self.buttonFrame, textvariable=self.btnText, command=self.OnPlayPause)

    def createFrame(self):
        self.panel = tk.Frame(self.root, width=480, height=290)
        self.panel.place(x=0, y=0)
        self.video = tk.Label(self.panel)

        self.buttonFrame = tk.Frame(self.root, width=480, height=30)
        self.buttonFrame.place(x=0, y=290)
        # self.text_box = tk.Text(self.buttonFrame, height=30, width=120)
        self.msgs = tk.StringVar()
        self.text_box = tk.Label(self.buttonFrame, textvariable=self.msgs)
        self.text_box.place(x=0, y=5)

    def destruct(self):
        if(self.cameraStatus == True):
            self.cameraStatus = False
            self.closeButton.place_forget()
            self.camera.destructor()

        else:
            self.player.stop()
            self.playpauseButton.place_forget()
            self.closeButton.place_forget()

        self.video.place_forget()
        self.openVidButton.place(relx=0.25, rely=0.5, width=80, anchor="w")
        self.openCamButton.place(relx=0.75, rely=0.5, width=80, anchor="e")

    def showCam(self):
        # self.createCamera()
        if(self.cameraStatus != True):
            self.camera = aruco(0)
            self.cameraStatus = True
            self.textStatus = False

            self.video.place(relx=0.5, rely=0.5, anchor="center")
            self.openVidButton.place_forget()
            self.openCamButton.place_forget()
            self.closeButton.place(relx=0.5, rely=0.5, anchor="center")

            self.processing()
        else:
            print("Video is still running...")

    def processing(self):
        self.frame, self.ids = self.camera.capture()
        self.frame = self.frame[:,:,::-1]
        current_image = Image.fromarray(self.frame)  # convert image for PIL
        resize_image = current_image.resize((416,290), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=resize_image)  # convert image for tkinter
        self.video.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.video.configure(image=imgtk)  # show the image
        
        if(self.ids is not None and (self.textStatus == False)):
            temp = "Aruco IDs : " + str(self.ids[0]) + " detected!"
            self.msgs.set(temp)
            self.textStatus = True
            
            
        elif (isinstance(self.ids, type(None)) and (self.textStatus == True)):
            temp = ""
            self.msgs.set(temp)
            self.textStatus = False

        self.video.after(10, self.processing)

    def showVideo(self, input):
        if(self.cameraStatus != True):
            self.video.place(relx=0.5, rely=0.5, anchor="center")

            instance = vlc.Instance()
            self.player = instance.media_player_new()
            media = instance.media_new(input)
            self.player.set_media(media)
            self.player.set_hwnd(self.video.winfo_id())

            self.openVidButton.place_forget()
            self.openCamButton.place_forget()

            self.playpauseButton.place(relx=0.5, rely=0.5, width=50, anchor="center")
            self.closeButton.place(relx=0.1, rely=0.5, anchor="w")
            # self.pauseButton.place(relx=0.5, rely=0.5, width=50, anchor="center")
            
            self.player.play()
            self.playStatus = True
            self.btnText.set("Pause")

        else:
            print("Error! Video still running...")

    def OnPlayPause(self):
        if (self.playStatus != True):
            self.player.play()
            temp = "Pause"
        else:
            self.player.pause()  
            temp = "Play"
        self.playStatus = not self.playStatus    
        self.btnText.set(temp)

    # def OnPlay(self):
    #     self.playStatus = True
    #     if self.player.play() == -1:
    #         self.errorDialog("Unable to play.")
    
    # def OnPause(self):
    #     self.playStatus = False
    #     self.player.pause()

    def destructor(self):
        self.root.destroy()

    def looping(self):
        self.root.mainloop()
	# 	
    
