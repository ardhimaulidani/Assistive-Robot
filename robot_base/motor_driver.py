# Motor Driver Library
# By Ardhika Maulidani
# Usage : For L298N/L293 Motor Driver paired with Raspberry Pi

# Define Library
import RPi.GPIO as GPIO
from time import time, sleep
import math

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define Motor Class
class motor():
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)

        self.PWM = GPIO.PWM(self.EN, 100)
        self.PWM.start(0)
        self.stop()

    def forward(self, speed):
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)
        self.PWM.ChangeDutyCycle(speed)

    def reverse(self, speed):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)
        self.PWM.ChangeDutyCycle(speed)

    def brake(self):
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 1)
        
    def stop(self):
        self.PWM.ChangeDutyCycle(0)

# Define Encoder Class
class encoder():
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