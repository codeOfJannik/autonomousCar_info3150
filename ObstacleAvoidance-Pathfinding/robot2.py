# External module imports
import RPi.GPIO as GPIO
import time

#Needed to import file located in different folder???
import sys
sys.path.insert(1, '../')

#from RTIMUScripts import get_heading
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

motor = Motor()
frontSensor = Ultrasonic()
leftFrontSensor = InfraredSensor(21)
rightFrontSensor = InfraredSensor(16)
leftSensor = InfraredSensor(12)
rightSensor = InfraredSensor(20)

components = [motor, frontSensor, leftSensor, leftFrontSensor, rightSensor, rightFrontSensor]

# # Functions for driving
# def goforward():
#     GPIO.output(11, True)
#     GPIO.output(15, True)
#
#
# def turnleft():
#     GPIO.output(11, True)
#     GPIO.output(15, False)
#     time.sleep(0.8)
#     GPIO.output(11, False)
#
#
# def turnright():
#     GPIO.output(15, True)
#     GPIO.output(11, False)
#     time.sleep(0.8)
#     GPIO.output(15, False)
#
#
# def gobackward():
#     GPIO.output(37, True)
#     GPIO.output(13, True)
#
#
# def stopmotors():
#     GPIO.output(15, False)
#     GPIO.output(11, False)
#     GPIO.output(37, False)
#     GPIO.output(13, False)


# Detect front obstacle
def frontobstacle():
    return frontSensor.sense()

def rightFrontObstacle():
    return rightFrontSensor.is_blocked_by_obstacle()

def leftFrontObstacle():
    return leftFrontSensor.is_blocked_by_obstacle()

def rightObstacle():
    return rightSensor.is_blocked_by_obstacle()

def leftObstacle():
    return leftSensor.is_blocked_by_obstacle()

def goBackUntilSpaceToTurnRight():
    while leftObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()
    if not rightFrontObstacle() and not rightObstacle():
        return
    else:
        while rightObstacle() or rightFrontObstacle():
            motor.backward()
            time.sleep(1)
            motor.stop()
        if leftObstacle():
            goBackUntilSpaceToTurnRight()

def goBackUntilSpaceToTurnLeft():
    while rightObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()
    if not leftFrontObstacle() and not leftObstacle():
        return
    else:
        while leftObstacle() or leftFrontObstacle():
            motor.backward()
            time.sleep(1)
            motor.stop()
        if rightObstacle():
            goBackUntilSpaceToTurnLeft()


# Check front obstacle and turn right if there is an obstacle
def checkanddrivefront():
    while (frontobstacle() < 15 or leftFrontObstacle()):
        if leftObstacle():
            goBackUntilSpaceToTurnRight()
        motor.turnRight()
        time.sleep(1)
        motor.stop()


# Check right obstacle and turn left if there is an obstacle
def checkanddriveright():
    while rightFrontObstacle() or frontobstacle() < 15:
        if leftObstacle():
            goBackUntilSpaceToTurnRight()
        motor.turnLeft()
        time.sleep(1)
        motor.stop()


# Check left obstacle and turn right if there is an obstacle
def checkanddriveleft():
    while leftFrontObstacle() or frontobstacle() < 15:
        if rightObstacle():
            goBackUntilSpaceToTurnLeft()
        motor.turnRight()
        time.sleep(1)
        motor.stop()


# Avoid obstacles and drive forward
def obstacleavoiddrive():
    start = time.time()
    # Drive 5 minutes
    while start > time.time() - 300:  # 300 = 60 seconds * 5
        motor.forward()
        if frontobstacle() < 10:
            print("if1")
            motor.stop()
            checkanddrivefront()
        elif rightFrontObstacle():
            print("if2")
            motor.stop()
            checkanddriveright()
        elif leftFrontObstacle():
            print("if3")
            motor.stop()
            checkanddriveleft()
    # Clear GPIOs, it will stop motors       
    cleargpios()


def cleargpios():
    print ("clearing GPIO")
    for component in components:
        del component


def main():
    print ("start driving: ")
    # Start obstacle avoid driving
    obstacleavoiddrive()
    

if __name__ == "__main__":
    main()

try:
    main()
except KeyboardInterrupt:
   cleargpios()
