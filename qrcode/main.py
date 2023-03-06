from aruco_read import aruco
from gui import gui

if __name__ == "__main__":
    try:
        gui = gui()
        gui.showCam()
        gui.looping()
    except KeyboardInterrupt :
         gui.destructor()
