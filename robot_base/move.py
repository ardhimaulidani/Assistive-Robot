# Robot Base Move Program
# By Ardhika Maulidani
# Package for controlling robot using Joystick 

from encoder import Encoder
from motor_driver import Motor
from pid import PID
import time

if __name__ == "__main__":
    motorLeft = Motor(17, 27, 13)
    motorRight = Motor(23, 24, 12)
    
    encoderLeft = Encoder(22)
    encoderRight = Encoder(25)

    pidLeft = PID(0.2, 0.00001, 0.0, 200, 0.05, (0, 100))
    pidRight = PID(0.2, 0.00001, 0.0, 200, 0.05, (0, 100))

    while True:
        rpmLeft = encoderLeft.get_rpm() 
        rpmRight = encoderRight.get_rpm()

        output = pidRight(rpmRight)

        motorLeft.forward(pidLeft(rpmLeft))
        motorRight.forward(output)
        print(rpmLeft, rpmRight)
