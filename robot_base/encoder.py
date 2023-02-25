# LM393 IR Encoder Library
# By Ardhika Maulidani
# Usage : For LM393 IR Encoder paired with Raspberry Pi

# Define Library
import RPi.GPIO as GPIO
import time
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
            self.counter += 1
            # print(self.counter)

        self.PIN = PIN
        self.counter = 0
        self.rpm = 0.00
        self.previousTime = self.millis()
        # print("called")
        GPIO.setup(PIN, GPIO.IN)
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=encoder_cb)
    
    def get_rpm(self):
        # print(self.millis())
        if (self.millis() - self.previousTime >= 50):
                # print("called")
                self.rpm = (self.counter/40)*1200
                self.counter = 0
                self.previousTime = self.millis()
        return self.rpm

    def get_velocity(self):
        self.rpm = self.get_rpm()
        w = (self.rpm*math.pi*2)/60
        v = w*(6.5/2)
        return (v)
    
    def millis(self):
         return (time.time()*1000)




