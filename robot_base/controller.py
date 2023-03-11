# Import the pygame module
import pygame
from pygame.locals import *

# Import hardware controller
from move import diff_drive

# Define constants for the screen width and height
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# Initialize pygame
pygame.init()
running = True
# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class joystick(object):
    def __init__(self):
        joycount = pygame.joystick.get_count()
        if joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            quit(1)
        self.temp = []
        for i in range(joycount):
            self.temp.append(self.joystick_handler(i))

    def joystick_handler(self, id):
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
        return self #for self chaining

    def get_joy(self):
        return (self.temp)

if __name__ == "__main__":
    gamepad = joystick()
    joy = gamepad.get_joy()

    drive = diff_drive(17, 27, 13, 23, 24, 12)

    while(running):
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

            elif event.type == JOYAXISMOTION:
                joy[event.joy].axis[event.axis] = event.value

            elif event.type == JOYBALLMOTION:
                joy[event.joy].ball[event.ball] = event.rel

            elif event.type == JOYHATMOTION:
                joy[event.joy].hat[event.hat] = event.value

            elif event.type == JOYBUTTONUP:
                joy[event.joy].button[event.button] = 0

            elif event.type == JOYBUTTONDOWN:
                joy[event.joy].button[event.button] = 1

        # Fill the screen with black
        screen.fill((0, 0, 0))

        a, b = drive.joystickToDiff(joy[0].axis[0], -joy[0].axis[1])
        # print(a, b)
        
        # Update the display
        pygame.display.flip()