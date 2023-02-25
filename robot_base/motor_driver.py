# Motor Driver Library
# By Ardhika Maulidani
# Usage : For L298N/L293 Motor Driver paired with Raspberry Pi

# Define Library
import RPi.GPIO as GPIO
from time import time, sleep

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define Motor Class
class Motor():
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