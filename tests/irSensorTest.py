from infraredSensor import InfraredSensor
import RPi.GPIO as gpio
import time
import sys
sys.path.insert(1, '../')

irSensorPinNumbers = [12, 16, 20, 21]
sensors = []

for pinNumber in irSensorPinNumbers:
    sensors.append(InfraredSensor(pinNumber))

try:
    print("start infrared sensor test")
    while True:
        for sensor in sensors:
            if sensor.is_blocked_by_obstacle():
                print("sensor at pin " + str(sensor.SENSORPIN) + " blocked by obstacle")
            else:
                print("sensor at pin " + str(sensor.SENSORPIN) + " free")
        time.sleep(2)
except KeyboardInterrupt:
    print("Quit")
    gpio.cleanup()
