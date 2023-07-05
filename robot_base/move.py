# Robot Base Move Program
# By Ardhika Maulidani
# Package for controlling robot using Joystick 

import math
import io

class moveDiff(object):
    def __init__(self, left_IN1, left_IN2, left_PWM, right_IN1, right_IN2, right_PWM):
        # Init Only if System is Raspberry Pi
        if self.is_raspberrypi():
            from motor_driver import motor
            self.motorLeft = motor(left_IN1, left_IN2, left_PWM)
            self.motorRight = motor(right_IN1, right_IN2, right_PWM)
        else:
            print("Failed to initiate motor driver. Program is running on different system")
            pass

    def joystickToDiff(self, x, y, maxSpeed=50):
        # Joystick Deadzone
        if (x >= -0.12 and x <= 0.12) and (y >= -0.12 and y <= 0.12):
            return(0, 0, 0)
        # Get Movement from Joystick
        else:
            try:
                rad = math.atan(y/x)
            except ZeroDivisionError:
                rad = math.radians(90)
                
            # Get Angle Value from Joystick
            angle = rad * 180 / math.pi
            mov = max(math.fabs(y), math.fabs(x))
            pwm = self.map(mov, 0, 1, 0, maxSpeed)

            # Divide Joystick into 4 Regions
            if(((angle >= -90 and angle <= -45) or (angle <=90 and angle >= 45)) and y>=0.12):
                return(1, 1, pwm)
            elif(((angle >= -90 and angle <= -45) or (angle <=90 and angle >= 45)) and y<=-0.12):
                return(-1, -1, pwm)
            elif((angle<=45 and angle>=-45) and x<=-0.12):
                return(0, 1, pwm)
            elif((angle<=45 and angle>=-45) and x>=0.12):
                return(1, 0, pwm)
                
    def move(self, x, y, pwm):
        # Diffential Movement from Analog
        if(self.is_raspberrypi()):
            if(x == 1 and y == 1):
                # Forward Move
                self.motorRight.forward(pwm)
                self.motorLeft.forward(pwm)

            elif(x == -1 and y == -1):
                # Backward Move
                self.motorRight.reverse(pwm)
                self.motorLeft.reverse(pwm)

            elif(x == 0 and y == 1):
                # Left Move
                self.motorRight.forward(pwm)
                self.motorLeft.reverse(pwm)

            elif(x == 1 and y == 0):
                # Right Move
                self.motorRight.reverse(pwm)
                self.motorLeft.forward(pwm)
            
            else:
                # Stop Move
                self.motorRight.stop()
                self.motorLeft.stop()  
        else:
            pass   

    def moveKeyboard(self, key):
        # Diffential Movement from Keyboard Keys
        if(self.is_raspberrypi()):
            if(key == "up"):
                # Forward Move
                self.motorRight.forward(15)
                self.motorLeft.forward(15)

            elif(key == "down"):
                # Backward Move
                self.motorRight.reverse(15)
                self.motorLeft.reverse(15)

            elif(key == "left"):
                # Left Move
                self.motorRight.forward(15)
                self.motorLeft.reverse(0)

            elif(key == "right"):
                # Right Move
                self.motorRight.reverse(0)
                self.motorLeft.forward(15)
            
            else:
                # Stop Move
                self.motorRight.stop()
                self.motorLeft.stop()  
        else:
            pass          
            
    def is_raspberrypi(self):
        # Check if Raspberry Pi is the System
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    return True
        except Exception: 
            pass
            return False

    def map(self, v, in_min, in_max, out_min, out_max):
        # Map Function for IN/OUT variables
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
