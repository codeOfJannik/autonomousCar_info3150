import RPi.GPIO as gpio
import time

class Motor:
    __MOTOR1A = 17
    __MOTOR1B = 22
    __MOTOR2A = 23
    __MOTOR2B = 24

    __Frequency = 20
    __DutyCycleA = 40
    __DutyCycleB = 40
    __Stop = 0

    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__MOTOR1A, gpio.OUT)
        gpio.setup(self.__MOTOR1B, gpio.OUT)
        gpio.setup(self.__MOTOR2A, gpio.OUT)
        gpio.setup(self.__MOTOR2B, gpio.OUT)
        self.pwmMOTOR1A = gpio.PWM(self.__MOTOR1A, self.__Frequency)
        self.pwmMOTOR1B = gpio.PWM(self.__MOTOR1B, self.__Frequency)
        self.pwmMOTOR2A = gpio.PWM(self.__MOTOR2A, self.__Frequency)
        self.pwmMOTOR2B = gpio.PWM(self.__MOTOR2B, self.__Frequency)
        self.pwmMOTOR1A.start(self.__Stop)
        self.pwmMOTOR1B.start(self.__Stop)
        self.pwmMOTOR2A.start(self.__Stop)
        self.pwmMOTOR2B.start(self.__Stop)

    def forward(self):
        self.pwmMOTOR1A.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__DutyCycleB)

    def backward(self):
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__DutyCycleB)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def turnRight(self):
        self.pwmMOTOR1A.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__DutyCycleB)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def turnLeft(self):
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__DutyCycleB)

    def stop(self):
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def __del__(self):
        gpio.cleanup()
