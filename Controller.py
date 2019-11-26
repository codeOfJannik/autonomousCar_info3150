import sys
sys.path.insert(1, './Library/scripts')

from RTIMUScripts import get_heading
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

motor = Motor()
right_ir_sensor = InfraredSensor(16)
left_ir_sensor = InfraredSensor(12)
right_front_ir_sensor = InfraredSensor(20)
left_front_ir_sensor = InfraredSensor(21)
ultrasonicSensor = Ultrasonic()

components = [motor, right_ir_sensor, left_ir_sensor, right_front_ir_sensor, left_front_ir_sensor, ultrasonicSensor]

car_stopped = False

def normalizeDegrees(degrees):
    if 0 <= degrees < 360:
        return degrees
    elif degrees < 0:
        return degrees + 360
    elif degrees >= 360:
        return degrees - 360


def turnDegrees(degrees):
    currentHeading = get_heading()
    print("Current heading: " + str(currentHeading))

    if degrees < 0:
        finalHeading = currentHeading + degrees
        finalHeading = normalizeDegrees(finalHeading)

        print("Heading after turning: " + str(finalHeading))

        motor.turnLeft()
        while True:
            heading = get_heading()
            print("Heading: " + str(heading))

            if heading < finalHeading:
                motor.stop()
                break
    else:
        finalHeading = currentHeading + degrees
        finalHeading = normalizeDegrees(finalHeading)

        print("Heading after turning: " + str(finalHeading))

        motor.turnRight()
        while True:
            heading = get_heading()
            print("Heading: " + str(heading))

            if heading > finalHeading:
                motor.stop()
                break

    startDriving()

def noObstacleAtFront():
    return ultrasonicSensor.sense() > 10.01

def driveBackwards():
    motor.backward()

def check_sides():
    if not right_ir_sensor.is_blocked_by_obstacle():
        print("right: no obstacle")
        turnDegrees(90)
    elif not left_ir_sensor.is_blocked_by_obstacle():
        print("right: obstacle")
        print("left: no obstacle")
        turnDegrees(-90)
    else:
        print("right: obstacle")
        print("left: obstacle")
        self.car_stopped = True
        print("stopped due dead end")
        for component in components:
            del component


def check_for_FrontObstacle():
    while True:
        if not noObstacleAtFront():
            print("obstacle in front detected")
            motor.stop()
            check_sides()

def check_for_BackObstacle():
    while True:
        if back_ir_sensor.is_blocked_by_obstacle():
            motor.stop()
            check_sides()

def driveForward():
    motor.forward()
    check_for_FrontObstacle()

def startDriving():
    print("Start driving")
    print("obstacle at the front: " + str(noObstacleAtFront()))
    if noObstacleAtFront():
        driveForward()
    else:
        check_sides()

try:
    startDriving()
except KeyboardInterrupt:
    car_stopped = True
    print ("Stopped by User")
    for component in components:
        del component
