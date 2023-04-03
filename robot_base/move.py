# Robot Base Move Program
# By Ardhika Maulidani
# Package for controlling robot using Joystick 

import math
import io

class moveDiff(object):
    def __init__(self, left_IN1, left_IN2, left_PWM, right_IN1, right_IN2, right_PWM):
        if self.is_raspberrypi():
            from motor_driver import motor
            self.motorLeft = motor(left_IN1, left_IN2, left_PWM)
            self.motorRight = motor(right_IN1, right_IN2, right_PWM)
        else:
            print("Failed to initiate motor driver. Program is running on different system")
            pass

    def joystickToDiff(self, x, y, maxSpeed=50):
        # Joystick Deadzone
        # print(x,y)
        if (x >= -0.12 and x <= 0.12) and (y >= -0.12 and y <= 0.12):
            return(0, 0, 0)
        
        else:
            try:
                rad = math.atan(y/x)
            except ZeroDivisionError:
                rad = math.radians(90)
                
            angle = rad * 180 / math.pi
            # max of y or x is the movement
            mov = max(math.fabs(y), math.fabs(x))
            pwm = self.map(mov, 0, 1, 0, maxSpeed)

            # Up Region
            if(((angle >= -90 and angle <= -45) or (angle <=90 and angle >= 45)) and y>=0.12):
                return(1, 1, pwm)
            elif(((angle >= -90 and angle <= -45) or (angle <=90 and angle >= 45)) and y<=-0.12):
                return(-1, -1, pwm)
            elif((angle<=45 and angle>=-45) and x<=-0.12):
                return(0, 1, pwm)
            elif((angle<=45 and angle>=-45) and x>=0.12):
                return(1, 0, pwm)
                
    def move(self, x, y, pwm):
        if(self.is_raspberrypi()):
            if(x == 1 and y == 1):
                self.motorRight.forward(pwm)
                self.motorLeft.forward(pwm)
                # print("FORWARD")

            elif(x == -1 and y == -1):
                self.motorRight.reverse(pwm)
                self.motorLeft.reverse(pwm)
                # print("BACKWARD")

            elif(x == 0 and y == 1):
                self.motorRight.forward(pwm)
                self.motorLeft.reverse(pwm)
                # print("LEFT")

            elif(x == 1 and y == 0):
                self.motorRight.reverse(pwm)
                self.motorLeft.forward(pwm)
                # print("RIGHT")
            
            else:
                self.motorRight.stop()
                self.motorLeft.stop()  
                # print("STOP") 
        else:
            pass   

    def moveKeyboard(self, key):
        if(self.is_raspberrypi()):
            if(key == "up"):
                self.motorRight.forward(15)
                self.motorLeft.forward(15)
                # print("FORWARD")

            elif(key == "down"):
                self.motorRight.reverse(15)
                self.motorLeft.reverse(15)
                # print("BACKWARD")

            elif(key == "left"):
                self.motorRight.forward(15)
                self.motorLeft.reverse(0)
                # print("LEFT")

            elif(key == "right"):
                self.motorRight.reverse(0)
                self.motorLeft.forward(15)
                # print("RIGHT")
            
            else:
                self.motorRight.stop()
                self.motorLeft.stop()  
                # print("STOP") 
        else:
            pass          
    def is_raspberrypi(self):
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    return True
        except Exception: 
            pass
            return False

    def map(self, v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
