import RPi.GPIO as gpio
import time

class InfraredSensors:
    __SENSOR1 = 12
    __SENSOR2 = 16
    __SENSOR3 = 20
    __SENSOR4 = 21
    
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__SENSOR1, gpio.IN)
        gpio.setup(self.__SENSOR2, gpio.IN)
        gpio.setup(self.__SENSOR3, gpio.IN)
        gpio.setup(self.__SENSOR4, gpio.IN)
        
    def sensor1Obstacle(self):
        try:
            while True:
                if not gpio.input(self.__SENSOR1):
                    print("Obstacle at sensor 1")
                time.sleep(1)
        except KeyboardInterrupt:
            print("quit")
            gpio.cleanup()
    