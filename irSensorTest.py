from infraredSensor import InfraredSensors
from RPi.GPIO import gpio
import time

irSensorPinNumbers = [12, 16, 20, 21]
sensors = []

for pinNumber in irSensorPinNumbers:
    sensors.append(InfraredSensor(pinNumber))

try:
    print("start infrared sensor test")
    while True:
        for sensor in sensors:
            print("sensor at pin " + str(sensor.SENSORPIN) + " blocked by obstacle")
        time.sleep(2)
except KeyboardInterrupt:
    print("Quit")
    gpio.cleanup()
