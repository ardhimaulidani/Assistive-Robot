# Import the PyGame Module
import pygame
from pygame.locals import *

# Import Hardware Controller
from move import moveDiff

# Define Screen Width and Height
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# Initialize PyGame
pygame.init()
running = True

# Create the Screen Object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class joystick(object):
  def __init__(self):
    # Init Joystick Object
    self.joycount = pygame.joystick.get_count()
    self.temp = []
    self.key = None

    # If Joystick is Not Detected
    if(self.joycount == 0):
      print("No joysticks were detected. Use keyboard control layout")
      self.temp.append(self.joystick_handler(-1))
      
    # Get Joystick ID
    else:
      for i in range(self.joycount):
          self.temp.append(self.joystick_handler(i))

  def joystick_handler(self, id):
    # Insert Dummy Object If Controller Not Detected
    if(id == -1):
      self.axis = [0,0,0,0,0,0]
      self.ball = [0,0,0,0]
      self.button = [0,0,0,0,0,0,0,0,0,0,0,0]
      self.hat = [0,0,0,0]
      return self
      
    # Create Controller Object
    else:
      self.id = id
      self.joy = pygame.joystick.Joystick(id)
      self.name = self.joy.get_name()
      self.joy.init()
      self.numaxes    = self.joy.get_numaxes()
      self.numballs   = self.joy.get_numballs()
      self.numbuttons = self.joy.get_numbuttons()
      self.numhats    = self.joy.get_numhats()

      self.axis = []
      for i in range(self.numaxes):
          self.axis.append(self.joy.get_axis(i))

      self.ball = []
      for i in range(self.numballs):
          self.ball.append(self.joy.get_ball(i))

      self.button = []
      for i in range(self.numbuttons):
          self.button.append(self.joy.get_button(i))

      self.hat = []
      for i in range(self.numhats):
          self.hat.append(self.joy.get_hat(i))
      return self # For Self-Chaining

  def get_control(self):
    self.isPressed = None
    for event in pygame.event.get():
      # Check for KEYDOWN event      
      self.key = pygame.key.get_pressed()
      if (event.type == pygame.KEYDOWN):
        # Check for pressed key
        if self.key[pygame.K_RIGHT]:
          self.key = "right"
        elif self.key[pygame.K_LEFT]:
          self.key = "left"
        elif self.key[pygame.K_UP]:
          self.key = "up"
        elif self.key[pygame.K_DOWN]:
          self.key = "down"
        elif self.key[pygame.K_ESCAPE]:
          pygame.quit()
          exit()
        elif self.key[pygame.K_RETURN]:
          self.key = "enter"
          self.isPressed = True
        elif self.key[pygame.K_SPACE]:
          self.key = "space"
          self.isPressed = True
        elif self.key[pygame.K_q]:
          self.key = "q"
          self.isPressed = True
        elif self.key[pygame.K_r]:
          self.key = "r"
          self.isPressed = True

      # Check for QUIT event
      elif event.type == QUIT:
        pygame.quit()
        exit()

      # Get Event if Joystick is Detected
      if(self.joycount >= 1):
        if event.type == JOYAXISMOTION:
          self.temp[event.joy].axis[event.axis] = event.value

        elif event.type == JOYBALLMOTION:
          self.temp[event.joy].ball[event.ball] = event.rel

        elif event.type == JOYHATMOTION:
          self.temp[event.joy].hat[event.hat] = event.value

        elif event.type == JOYBUTTONUP:
          self.temp[event.joy].button[event.button] = 0

        elif event.type == JOYBUTTONDOWN:
          self.isPressed = True
          self.temp[event.joy].button[event.button] = 1
      else:
        pass

    return(self.key, self.isPressed, self.temp)
