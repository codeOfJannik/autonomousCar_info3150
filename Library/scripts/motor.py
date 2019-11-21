import RPi.GPIO as gpio

class Motor:
    __MOTOR1A = 17
    __MOTOR1B = 22
    __MOTOR2A = 23
    __MOTOR2B = 24

    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__MOTOR1A, gpio.OUT)
        gpio.setup(self.__MOTOR1B, gpio.OUT)
        gpio.setup(self.__MOTOR2A, gpio.OUT)
        gpio.setup(self.__MOTOR2B, gpio.OUT)

    def forward(self):
        gpio.output(self.__MOTOR1A, True)
        gpio.output(self.__MOTOR1B, False)
        gpio.output(self.__MOTOR2A, False)
        gpio.output(self.__MOTOR2B, True)

    def backward(self):
        gpio.output(self.__MOTOR1A, False)
        gpio.output(self.__MOTOR1B, True)
        gpio.output(self.__MOTOR2A, True)
        gpio.output(self.__MOTOR2B, False)

    def turnRight(self):
        gpio.output(self.__MOTOR1A, True)
        gpio.output(self.__MOTOR1B, False)
        gpio.output(self.__MOTOR2A, True)
        gpio.output(self.__MOTOR2B, False)

    def turnLeft(self):
        gpio.output(self.__MOTOR1A, False)
        gpio.output(self.__MOTOR1B, True)
        gpio.output(self.__MOTOR2A, False)
        gpio.output(self.__MOTOR2B, True)

    def stop(self):
        gpio.output(self.__MOTOR1A, False)
        gpio.output(self.__MOTOR1B, False)
        gpio.output(self.__MOTOR2A, False)
        gpio.output(self.__MOTOR2B, False)

    def __del__(self):
        gpio.cleanup()
