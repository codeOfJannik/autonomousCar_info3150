from RTIMUScripts import get_heading
from motor import Motor
import time

try:
   while True:
       print(str(get_heading()))
       time.sleep(2)
except KeyboardInterrupt:
    print("Quit")

def driving_compass_test():
    motor = Motor()

    motor.forward()
    time.sleep(1)
    motor.stop()

    currentDirection = get_heading()
    print("current direction: " + str(currentDirection))
    finalDirection = currentDirection + 90 if currentDirection + 90 < 360 else currentDirection + 90 - 360
    print("final direction: " + str(currentDirection))

    try:
        motor.turnRight()
        while True:
            currentDirection = get_heading()
            print("current direction: " + str(currentDirection))

            if currentDirection >= finalDirection:
                motor.stop()
                motor.__del__()
                currentDirection = get_heading()
                print("current direction: " + str(currentDirection))
                break
    except KeyboardInterrupt:
        motor.stop()
        motor.__del__()

