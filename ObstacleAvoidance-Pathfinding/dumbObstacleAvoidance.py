# External module imports
import RPi.GPIO as GPIO
import time
import random

#Needed to import file located in different folder???
import sys
sys.path.insert(1, '../')

#from RTIMUScripts import get_heading
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

wheels = Motor()
frontSensor = Ultrasonic()
frontLeftSensor = InfraredSensor(21)
frontRightSensor = InfraredSensor(16)
backLeftSensor = InfraredSensor(12)
backRightSensor = InfraredSensor(20)

components = [wheels, frontSensor, backLeftSensor, frontLeftSensor, backRightSensor, frontRightSensor]

def randomLeftRight():
    bool = bool(random.getrandbits(1))
    if bool is True:
        wheels.turnLeft()
        print("LEFT TURN")
        return bool
    else:
        wheels.turnRight()
        print ("RIGHT TURN")
        return bool

def frontObstacle():
    if frontSensor.sense() <= 15.0:
        time.sleep(0.01)
        print ("FRONT CLEAR")
        return True
    else:
        print ("FRONT BLOCKED")
        return False

def frontRightObstacle():
    if frontRightSensor.is_blocked_by_obstacle():
        print ("FRONT RIGHT BLOCKED")
        return True
    else:
        print ("FRONT RIGHT CLEAR")
        return False

def frontLeftObstacle():
    if frontLeftSensor.is_blocked_by_obstacle():
        print ("FRONT LEFT BLOCKED")
        return True
    else:
        print ("FRONT LEFT CLEAR")
        return False

def backRightObstacle():
    if backRightSensor.is_blocked_by_obstacle():
        print ("BACK RIGHT BLOCKED")
        return True
    else:
        print ("BACK RIGHT CLEAR")
        return False

def backLeftObstacle():
    if backLeftSensor.is_blocked_by_obstacle():
        print ("BACK LEFT BLOCKED")
        return True
    else:
        print ("BACK LEFT CLEAR")
        return False

def obstacleAvoid():
    while True:
        wheels.forward()
        if frontObstacle():
            while frontObstacle() or frontLeftObstacle():
                wheels.turnRight()
                continue
        if frontLeftObstacle():
            wheels.backward()
            time.sleep(1)
            wheels.turnRight()
            time.sleep(1)
            continue
        if frontRightObstacle():
            wheels.backward()
            time.sleep(1)
            wheels.turnLeft()
            time.sleep(1)
            continue
        if (backRightObstacle() and backLeftObstacle()) and frontObstacle():
            while not backRightObstacle() and not backLeftObstacle():
                wheels.backward()
            wheels.backward()
            time.sleep(1)
            wheels.turnLeft()
            time.sleep(1)
            continue

def goBackUntilSpaceToTurnRight():
    while backLeftObstacle():
        wheels.backward()
        time.sleep(1)
        wheels.stop()
    if not frontRightObstacle() and not backRightObstacle():
        return
    else:
        while backRightObstacle() or frontRightObstacle():
            wheels.backward()
            time.sleep(1)
            wheels.stop()
        if backLeftObstacle():
            goBackUntilSpaceToTurnRight()

def goBackUntilSpaceToTurnLeft():
    while backRightObstacle():
        wheels.backward()
        time.sleep(1)
        wheels.stop()
    if not frontLeftObstacle() and not backLeftObstacle():
        return
    else:
        while backLeftObstacle() or frontLeftObstacle():
            wheels.backward()
            time.sleep(1)
            wheels.stop()
        if backRightObstacle():
            goBackUntilSpaceToTurnLeft()


# Check front obstacle and turn right if there is an obstacle
def checkanddrivefront():
    while (frontObstacle() < 15 or frontLeftObstacle()):
        if backLeftObstacle():
            goBackUntilSpaceToTurnRight()
        wheels.turnRight()
        time.sleep(1)
        wheels.stop()


# Check right obstacle and turn left if there is an obstacle
def checkanddriveright():
    while frontRightObstacle() or frontObstacle() < 15:
        if backLeftObstacle():
            goBackUntilSpaceToTurnRight()
        wheels.turnLeft()
        time.sleep(1)
        wheels.stop()


# Check left obstacle and turn right if there is an obstacle
def checkanddriveleft():
    while frontLeftObstacle() or frontObstacle() < 15:
        if backRightObstacle():
            goBackUntilSpaceToTurnLeft()
        wheels.turnRight()
        time.sleep(1)
        wheels.stop()


# Avoid obstacles and drive forward
def obstacleavoiddrive():
    wheels.forward()
    start = time.time()
    # Drive 5 minutes
    while start > time.time() - 300:  # 300 = 60 seconds * 5
        wheels.forward()
        if frontObstacle() < 10:
            print("if1")
            wheels.stop()
            checkanddrivefront()
        elif frontRightObstacle():
            print("if2")
            wheels.stop()
            checkanddriveright()
        elif frontLeftObstacle():
            print("if3")
            wheels.stop()
            checkanddriveleft()
    # Clear GPIOs, it will stop motors
    cleanGPIO()


def cleanGPIO():
    print ("GPIO CLEANED")
    for component in components:
        del component


def main():
   obstacleAvoid()


if __name__ == "__main__":
    main()

try:
    main()
except KeyboardInterrupt:
   cleanGPIO()
