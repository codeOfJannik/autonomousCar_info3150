from compassClass import Compass
from motor import Motor
import time

compass = Compass()

try:
   compass.measurment_function()
   while True:
       print(str(compass.heading))
except KeyboardInterrupt:
    print("Quit")

def driving_compass_test():
    compass = Compass()
    motor = Motor()

    motor.forward()
    time.sleep(1)
    motor.stop()

    currentDirection = compass.get_heading()
    print("current direction: " + str(currentDirection))
    finalDirection = currentDirection + 90 if currentDirection + 90 < 360 else currentDirection + 90 - 360
    print("final direction: " + str(currentDirection))

    try:
        motor.turnRight()
        while True:
            currentDirection = compass.get_heading()
            print("current direction: " + str(currentDirection))

            if currentDirection >= finalDirection:
                motor.stop()
                motor.__del__()
                currentDirection = compass.get_heading()
                print("current direction: " + str(currentDirection))
                break
    except KeyboardInterrupt:
        motor.stop()
        motor.__del__()

