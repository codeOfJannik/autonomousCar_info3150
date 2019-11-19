from navigationSensor import NavigationSensor
from motor import Motor
import time

import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import math

def convert_fusion_value_to_positive_bearing(fusionValue):
        if fusionValue < 0:
            return 360 + fusionValue
        return fusionValue

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

try:
    while True:
        if imu.IMURead():
            data = imu.getIMUData()
            print(data)
            #fusionPose = data["compass"]
            #print("r: %f p: %f y: %f" % (fusionPose[0], fusionPose[1], fusionPose[2]))
            #bearTo = math.degrees(fusionPose[2])
            #print(str(convert_fusion_value_to_positive_bearing(bearTo)))
            break
        time.sleep(poll_interval * 1.0 / 1000.0)
        
except KeyboardInterrupt:
    print("Quit")

def driving_compass_test():
    navigationSensor = NavigationSensor()
    motor = Motor()

    motor.forward()
    time.sleep(1)
    motor.stop()

    currentDirection = navigationSensor.get_compass_value()
    print("current direction: " + str(currentDirection))
    finalDirection = currentDirection + 90 if currentDirection + 90 < 360 else currentDirection + 90 - 360
    print("final direction: " + str(currentDirection))

    try:
        motor.turnRight()
        while True:
            currentDirection = navigationSensor.get_compass_value()
            print("current direction: " + str(currentDirection))

            if currentDirection >= finalDirection:
                motor.stop()
                motor.__del__()
                currentDirection = navigationSensor.get_compass_value()
                print("current direction: " + str(currentDirection))
                break
    except KeyboardInterrupt:
        motor.stop()
        motor.__del__()

