import tkinter as tk
from PIL import Image, ImageTk
import vlc
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
        
        self.pauseButton = tk.Button(self.buttonFrame, text="Pause", command=self.OnPause)
        self.playButton = tk.Button(self.buttonFrame, text="Play", command=self.OnPlay)

    def createFrame(self):
        self.panel = tk.Frame(self.root, width=480, height=290)
        self.panel.place(x=0, y=0)
        self.video = tk.Label(self.panel)

        self.buttonFrame = tk.Frame(self.root, width=480, height=30)
        self.buttonFrame.place(x=0, y=290)


    def destruct(self):
        if(self.cameraStatus == True):
            self.cameraStatus = False
            self.closeButton.place_forget()
            self.camera.destructor()

        else:
            self.player.stop()
            self.pauseButton.place_forget()
            self.playButton.place_forget()
            self.closeButton.place_forget()

        self.video.place_forget()
        self.openVidButton.place(relx=0.25, rely=0.5, width=80, anchor="w")
        self.openCamButton.place(relx=0.75, rely=0.5, width=80, anchor="e")

    def showCam(self):
        # self.createCamera()
        if(self.cameraStatus != True):
            self.camera = aruco(0)
            self.cameraStatus = True

            self.video.place(relx=0.5, rely=0.5, anchor="center")
            self.openVidButton.place_forget()
            self.openCamButton.place_forget()
            self.closeButton.place(relx=0.5, rely=0.5, anchor="center")

            self.processing()
        else:
            print("Video is still running...")

    def processing(self):
        self.frame = self.camera.capture()
        self.frame = self.frame[:,:,::-1]
        current_image = Image.fromarray(self.frame)  # convert image for PIL
        resize_image = current_image.resize((416,290), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=resize_image)  # convert image for tkinter
        self.video.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.video.configure(image=imgtk)  # show the image
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
            
            self.pauseButton.place(relx=0.39, rely=0.5, width=50, anchor="w")
            self.playButton.place(relx=0.51, rely=0.5, width=50, anchor="w")
            self.closeButton.place(relx=0.95, rely=0.5, width=50, anchor="e")

            self.player.play()
        else:
            print("Error! Video still running...")
        
    def OnPlay(self):
        if self.player.play() == -1:
            self.errorDialog("Unable to play.")
    
    def OnPause(self):
        self.player.pause()

    def destructor(self):
        self.root.destroy()

    def looping(self):
        self.root.mainloop()
	# 	
    
