import sys
sys.path.insert(1, './Library/scripts')

from compassScript import compass_script
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

motor = Motor()
right_ir_sensor = InfraredSensor(12)
left_ir_sensor = InfraredSensor(16)
right_front_ir_sensor = InfraredSensor(20)
left_front_ir_sensor = InfraredSensor(21)
ultrasonicSensor = Ultrasonic()

components = [motor, right_ir_sensor, left_ir_sensor, right_front_ir_sensor, left_front_ir_sensor, ultrasonicSensor]

def noObstacleAtFront():
    return ultrasonicSensor.sense() > 10.01

def turnDegrees(degrees):
    if degrees < 0:
        finalHeading = compass_script() + degrees
        motor.turnLeft()
        while True:
            if compass_script() < finalHeading:
                motor.stop()
                break
    else:
        finalHeading = compass_script() + degrees
        motor.turnRight()
        while True:
            if compass_script() > finalHeading:
                motor.stop()
                break

    if noObstacleAtFront():
        driveForward()
    else:
        check_sides()


def driveBackwards():
    motor.backward()

def check_sides():
    if not right_ir_sensor.is_blocked_by_obstacle():
        turnDegrees(90)
    elif not left_ir_sensor.is_blocked_by_obstacle():
        turnDegrees(-90)
    else:
        print("stopped due dead end")
        for component in components:
            del component


def check_for_FrontObstacle():
    while True:
        if not noObstacleAtFront():
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

try:
    if noObstacleAtFront():
        driveForward()
    else:
        check_sides()
except KeyboardInterrupt:
    print ("Stopped by User")
    for component in components:
        del component