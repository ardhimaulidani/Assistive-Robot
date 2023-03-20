# Robot Base Move Program
# By Ardhika Maulidani
# Package for controlling robot using Joystick 

import math
import io

class diff_drive(object):
    def __init__(self, left_IN1, left_IN2, left_PWM, right_IN1, right_IN2, right_PWM):
        if self.is_raspberrypi():
            from motor_driver import motor
            self.motorLeft = motor(left_IN1, left_IN2, left_PWM)
            self.motorRight = motor(right_IN1, right_IN2, right_PWM)
        else:
            print("Failed to initiate motor driver. Program is running on different system")
            pass

    def joystickToDiff(self, x, y, minJoystick=-1.0, maxJoystick=1.0, minSpeed=-50, maxSpeed=50):
        # Joystick Deadzone
        if (x >= -0.12 and x <= 0.12) and (y >= -0.12 and y <= 0.12):
            return (0, 0)

        # First Compute the angle in deg
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(math.fabs(x) / z)

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the coeff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
        turn = round(turn * 100, 0) / 100

        # And max of y or x is the movement
        mov = max(math.fabs(y), math.fabs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = mov
            rawRight = turn
        else:
            rawRight = mov
            rawLeft = turn

        # Reverse polarity
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0 - rawRight

        rightOut = self.map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
        leftOut = self.map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

        return (rightOut, leftOut)
    
    def move(self, x, y):
        if(x > 0):
            self.motorLeft.forward(x)
        elif(x == 0):
            self.motorLeft.stop()
        else:
            self.motorLeft.reverse(abs(x))

        if(y > 0):
            self.motorRight.forward(y)
        elif(y == 0):
            self.motorRight.stop()
        else:
            self.motorRight.reverse(abs(y))        

    def is_raspberrypi(self):
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): return True
        except Exception: pass
        return False

    def map(self, v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
# if __name__ == "__main__":
    # motorLeft = motor(17, 27, 13)
    # motorRight = motor(23, 24, 12)
    
    # encoderLeft = Encoder(22)
    # encoderRight = Encoder(25)

    # pidLeft = PID(0.2, 0.00001, 0.0, 200, 0.05, (0, 100))
    # pidRight = PID(0.2, 0.00001, 0.0, 200, 0.05, (0, 100))

    # while True:
        
        # rpmLeft = encoderLeft.get_rpm() 
        # rpmRight = encoderRight.get_rpm()

        # output = pidRight(rpmRight)

        # motorLeft.forward(pidLeft(rpmLeft))
        # motorRight.forward(output)
        # print(rpmLeft, rpmRight)
