import sys
import pygame
from pygame.locals import *

# Insert Include Path
sys.path.insert(0, 'qrcode')
from gui import Video, Camera, Start, Tutorial

sys.path.insert(0, 'robot_base')
from controller import joystick
from move import moveDiff

#  Define GUI Window Size
WIN_DISPLAY_WIDTH   = 480
WIN_DISPLAY_HEIGHT  = 320

VID_DISPLAY_WIDTH   = 352
VID_DISPLAY_HEIGHT  = 240

# Init PyGame
pygame.init()
running = True

# Change Taskbar Icon and Caption
programIcon = pygame.image.load('bin/icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Assistive Robot App - v0.75b')

# Init Display Size and Clock
win = pygame.display.set_mode((WIN_DISPLAY_WIDTH, WIN_DISPLAY_HEIGHT))
clock = pygame.time.Clock()

# Init Video Dictionaries
vidDicts = {
  0: "media/test.m4v",
  1: "media/1.m4v",
  2: "media/1.m4v",
  3: "media/1.m4v"
}

if __name__ == "__main__":

  # Initialize Joystick
  gamepad = joystick()

  # Initialize Robot Hardware
  drive = moveDiff(17, 27, 13, 23, 24, 12)

  # your program frame rate does not affect video playback
  clock.tick(60)
  
  # Initialize Start Screen
  startScreen = Start()
  tutorialScreen = Tutorial()
  startStatus = True

  while startStatus:
    key, isPressed, joy = gamepad.get_control()
    startScreen.draw(win, (0,0))
    pygame.display.update()
  
    # Control Layout
    if (key == "enter" or (joy[0].button[9] == 1 and isPressed == True)):
      tutorialStatus = True
      startScreen = False
      win.fill(pygame.Color("black"))
      break    
  
  while tutorialStatus:
    key, isPressed, joy = gamepad.get_control()
    tutorialScreen.draw(win, (0,0))
    pygame.display.update()
    
    # Control Layout
    if (key == "space" or (joy[0].button[0] == 1 and isPressed == True)):
      tutorialStatus = False
      camStatus = True
      win.fill(pygame.Color("black"))
      break  

  while(1):
    while camStatus:
      # Initialize Camera View
      cam = Camera(0)
      camStatus = True
      while(1):
        # Initialize Control Input
        key, isPressed, joy = gamepad.get_control()
    
        # Show Camera View on pygame frame
        ids = cam.processing()
        
        # Convert joystick to pwm
        x, y, pwm = drive.joystickToDiff(joy[0].axis[0], -joy[0].axis[1], 35)
        drive.move(x, y, pwm)

        cam.draw(win, (80, 40), force_draw=False)
        pygame.display.update()

        # Control Layout
        if ((key == "space" or (joy[0].button[0] == 1 and isPressed)) and ids is not None):
          print(int(ids))
          camStatus = False
          cam.close()
          win.fill(pygame.Color("black"))
          break     

    while camStatus is False:
      # provide video class with the path to your video
      vid = Video(vidDicts[int(ids)])
      vid.set_size((VID_DISPLAY_WIDTH, VID_DISPLAY_HEIGHT))

      while(1):
        # Initialize Control Input
        key, isPressed, joy = gamepad.get_control()

        # draws the video to the given surface, at the given position
        vid.draw(win, ((WIN_DISPLAY_WIDTH-VID_DISPLAY_WIDTH)/2,(WIN_DISPLAY_HEIGHT-VID_DISPLAY_HEIGHT)/2))
        pygame.display.update()

        # Control Layout
        if (key == "q" or (joy[0].button[2] == 1 and isPressed == True)):
            camStatus = True
            vid.close()
            win.fill(pygame.Color("black"))
            break
        elif (key == "r" or (joy[0].button[1] == 1 and isPressed == True)):
          vid.restart()           #rewind video to beginning when r or triangle is pressed
        elif (key == "space" or (joy[0].button[0] == 1 and isPressed == True)):
          vid.toggle_pause()      #pause/plays video
        elif key == "right":
          vid.seek(15)            #skip 15 seconds in video
        elif key == "left":
          vid.seek(-15)           #rewind 15 seconds in video
        elif key == "up":
          vid.set_volume(1.0)     #max volume
        elif key == "down":
          vid.set_volume(0.0)     #min volume

 