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
    ultrasonicOutput = frontSensor.sense()
    if frontSensor.latestValidUltrasonicDistance == 0:
        frontSensor.latestValidUltrasonicDistance = ultrasonicOutput
        return ultrasonicOutput
    if ultrasonicOutput - frontSensor.latestValidUltrasonicDistance > 50:
        motor.stop()
        ultrasonicOutput = waitForValidUltrasonicValue()
    frontSensor.latestValidUltrasonicDistance = ultrasonicOutput
    time.sleep(.05)
    return ultrasonicOutput

def rightFrontObstacle():
    return rightFrontSensor.is_blocked_by_obstacle()

def leftFrontObstacle():
    return leftFrontSensor.is_blocked_by_obstacle()

def rightObstacle():
    return rightSensor.is_blocked_by_obstacle()

def leftObstacle():
    return leftSensor.is_blocked_by_obstacle()

def goBackUntilSpaceToTurnRight():
    startObstacleTime = time.time()
    while leftObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()
        if time.time() - startObstacleTime > 11:
            turnAwayFromRightBorder()
            return
    if not rightFrontObstacle() and not rightObstacle():
        motor.backward()
        time.sleep(.5)
        motor.stop()
        return
    else:
        while rightObstacle() or rightFrontObstacle():
            motor.backward()
            time.sleep(1)
            motor.stop()
        if leftObstacle():
            goBackUntilSpaceToTurnRight()

def goBackUntilSpaceToTurnLeft():
    startObstacleTime = time.time()
    while rightObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()
        if time.time() - startObstacleTime > 11:
            turnAwayFromRightBorder()
            return
    if not leftFrontObstacle() and not leftObstacle():
        motor.backward()
        time.sleep(.5)
        motor.stop()
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

def waitForValidUltrasonicValue():
    ultrasonicValue = frontSensor.sense()
    counter = 0
    while ultrasonicValue - frontSensor.latestValidUltrasonicDistance > 200:
        print(str(ultrasonicValue) + ">" + str(frontSensor.latestValidUltrasonicDistance))
        counter += 1
        print(counter)
        if counter == 50:
            print("new value " + str(ultrasonicValue) + "seems to be true")
            break
    return ultrasonicValue

def turnAwayFromRightBorder():
    motor.stop()
    while leftObstacle() or leftFrontObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()

    turnCounter = 10
    while turnCounter > 0:
        motor.turnLeft()
        time.sleep(1/turnCounter)
        motor.stop()
        motor.forward()
        time.sleep(1/turnCounter)
        turnCounter -= 1

def turnAwayFromLeftBorder():
    motor.stop()
    while rightObstacle() or rightFrontObstacle():
        motor.backward()
        time.sleep(1)
        motor.stop()

    turnCounter = 10
    while turnCounter > 0:
        motor.turnRight()
        time.sleep(1 / turnCounter)
        motor.stop()
        motor.forward()
        time.sleep(1 / turnCounter)
        turnCounter -= 1

# Avoid obstacles and drive forward
def obstacleavoiddrive():
    motor.forward()
    start = time.time()
    # Drive 5 minutes
    obstacleRightStart = 0
    obstacleLeftStart = 0
    while start > time.time() - 300:  # 300 = 60 seconds * 5
        motor.forward()
        if frontobstacle() < 15:
            motor.stop()
            checkanddrivefront()
            obstacleRightStart = 0
            obstacleLeftStart = 0
            continue
        elif rightFrontObstacle():
            motor.stop()
            checkanddriveright()
            obstacleRightStart = 0
            obstacleLeftStart = 0
            continue
        elif leftFrontObstacle():
            motor.stop()
            checkanddriveleft()
            obstacleRightStart = 0
            obstacleLeftStart = 0
            continue

        if rightObstacle():
            if obstacleRightStart == 0:
                obstacleRightStart = time.time()
            elif time.time() - obstacleRightStart > 8:
                print ("Right border")
                turnAwayFromRightBorder()
                obstacleRightStart = 0
        else:
            if not obstacleRightStart == 0:
                obstacleRightStart = 0

        if leftObstacle():
            if obstacleLeftStart == 0:
                obstacleLeftStart = time.time()
            elif time.time() - obstacleLeftStart > 8:
                print ("Left border")
                turnAwayFromLeftBorder()
                obstacleLeftStart = 0
        else:
            if not obstacleLeftStart == 0:
                obstacleLeftStart = 0


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
