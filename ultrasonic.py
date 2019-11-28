import RPi.GPIO as gpio
import time

class Ultrasonic:
    __trig = 19
    __echo = 26

    latestValidUltrasonicDistance = 0


    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.__trig, gpio.OUT)
        gpio.setup(self.__echo, gpio.IN)
        gpio.output(self.__trig, False)

        print ("Waiting For Sensor")
        time.sleep(2)


    def sense(self):
        gpio.output(self.__trig, True)
        time.sleep(0.00001)
        gpio.output(self.__trig, False)

        while gpio.input(self.__echo) == 0: start = time.time()
        while gpio.input(self.__echo) == 1: end = time.time()

        duration = end - start
        distance = duration * 17150

        distance = round(distance, 2)
        print("FRONT DISTANCE: " + distance + " CM")
        return distance

    def cleanup(self):
        gpio.cleanup()

    def __del__(self):
        gpio.cleanup()
