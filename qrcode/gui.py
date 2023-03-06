import tkinter as tk
from PIL import Image, ImageTk
import vlc
from aruco_read import aruco

class gui(object):
    def __init__(self):
        self.camera = aruco(0)
        self.cameraStatus = False
        self.root = tk.Tk()
        self.root.title("Assistive Robot App")
        self.root.geometry("480x320")
        # self.root.resizable(False, False)
        # self.root.wm_attributes("-topmost", 1)
        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.createFrame()
        self.InitButton()
    
    def InitButton(self):
        self.openVidButton = tk.Button(self.root, text="Open Video", command=lambda : self.showVideo("video.mp4"))
        self.openCamButton = tk.Button(self.root, text="Open Camera", command=self.showCam)        
        self.closeButton = tk.Button(self.root, text="Close", command=self.destruct)
        self.pauseButton = tk.Button(self.root, text="Pause", command=self.OnPause)
        self.playButton = tk.Button(self.root, text="Play", command=self.OnPlay)

    def createFrame(self):
        self.video = tk.Label(self.root)
        self.panel = tk.Frame(self.root) 

    def destruct(self):
        if(self.cameraStatus == True):
            self.cameraStatus = False
            self.video.pack_forget()
            self.closeButton.pack_forget()
            self.camera.destructor()

        else:
            self.player.stop()
            self.panel.pack_forget()
            self.pauseButton.pack_forget()
            self.playButton.pack_forget()
            self.closeButton.pack_forget()

        self.openVidButton.pack(side=tk.LEFT)
        self.openCamButton.pack(side=tk.LEFT)

    def showCam(self):
        # self.createCamera()
        if(self.cameraStatus != True):
            self.camera = aruco(0)
            self.cameraStatus = True

            self.video.pack(fill=tk.BOTH,expand=1)
            self.openVidButton.pack_forget()
            self.openCamButton.pack_forget()
            self.closeButton.pack(side=tk.LEFT)
            
            self.processing()
        else:
            print("Video is still running...")

    def processing(self):
        self.frame = self.camera.capture()
        self.frame = self.frame[:,:,::-1]
        current_image = Image.fromarray(self.frame)  # convert image for PIL
        imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter
        self.video.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.video.configure(image=imgtk)  # show the image
        self.video.after(10, self.processing)

    def showVideo(self, input):
        if(self.cameraStatus != True):
            self.panel.pack(fill=tk.BOTH,expand=1)

            instance = vlc.Instance()
            self.player = instance.media_player_new()
            media = instance.media_new(input)
            self.player.set_media(media)
            self.player.set_hwnd(self.panel.winfo_id())

            self.openVidButton.pack_forget()
            self.openCamButton.pack_forget()
            
            self.pauseButton.pack(side=tk.LEFT, padx="11px")
            self.playButton.pack(side=tk.LEFT, padx="11px")
            self.closeButton.pack(side=tk.RIGHT, padx="11px")

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
    
