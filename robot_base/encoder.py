# LM393 IR Encoder Library
# By Ardhika Maulidani
# Usage : For LM393 IR Encoder paired with Raspberry Pi

# Define Library
import RPi.GPIO as GPIO
from time import time
import signal
import sys
import math

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define Encoder Class
class Encoder():
    def __init__(self, PIN):
        def encoder_cb(channel):
            self.counter =+ self.counter

        self.PIN = PIN
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=encoder_cb)
    
    def get_rpm(self):
        self.previousTime = time.time()
        if (time.time() - self.previousTime >= 1000):
                self.rpm = (self.counter/20)*60;      
                self.counter = 0;
                self.previousTime = time.time();
        return (self.rpm)

    def get_velocity(self):
        self.rpm = Encoder.get_rpm()
        self.w = (self.rpm*math.pi*2)/60
        self.v = w*4.13
        return (self.v)




