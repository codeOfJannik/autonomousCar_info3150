import RPi.GPIO as gpio

class Motor:
    __MOTOR1A = 17
    __MOTOR1B = 22
    __MOTOR2A = 23
    __MOTOR2B = 24

    __Frequency = 20
    #change if car doesnt drive straight 
    __DutyCycleA = 25
    __DutyCycleB = 25
    __DutyCycleT = 20
    __Stop = 0

    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
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
        print("Start driving forward")
        self.pwmMOTOR1A.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__DutyCycleB)

    def backward(self):
        print("Start driving backward")
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__DutyCycleA)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__DutyCycleB)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def turnLeft(self):
        print("Start turning left")
        self.pwmMOTOR1A.ChangeDutyCycle(self.__DutyCycleT)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__DutyCycleT)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def turnRight(self):
        print("Start turning right")
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__DutyCycleT)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__DutyCycleT)

    def stop(self):
        print("Motors stopping")
        self.pwmMOTOR1A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR1B.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2A.ChangeDutyCycle(self.__Stop)
        self.pwmMOTOR2B.ChangeDutyCycle(self.__Stop)

    def __del__(self):
        gpio.cleanup()
