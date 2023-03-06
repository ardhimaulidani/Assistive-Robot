from aruco_read import aruco
from gui import gui

if __name__ == "__main__":
    try:
        # vision = aruco(0)
        gui = gui()
        # gui.showVideo("video.mp4")
        gui.showCam()
        gui.looping()
    except KeyboardInterrupt :
         gui.destructor()
        #  vision.destructor()
