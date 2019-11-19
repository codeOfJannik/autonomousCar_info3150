from navigationSensor import NavigationSensor
from motor import Motor
import time

navigationSensor = NavigationSensor()

try:
    while True:
        bearTo = navigationSensor.get_compass_value()
        print(str(bearTo))
        time.sleep(0.5)
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

