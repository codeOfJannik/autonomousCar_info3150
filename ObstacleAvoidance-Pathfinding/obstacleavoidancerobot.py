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

motor = Motor();
<<<<<<< HEAD
FRONT_SENSOR_TRIGGER = 19
FRONT_SENSOR_ECHO = 26
frontSensor = Ultrasonic()
=======
frontSensor = Ultrasonic();
>>>>>>> ae4a5be47e25296c3641fc4dcbfcb464a57edd5d
leftSensor = InfraredSensor(21)
rightSensor = InfraredSensor(20)

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
<<<<<<< HEAD
    return frontSensor.sense()
=======

    # Set trigger to False (Low)
    frontSensor.GPIO.output(FRONT_SENSOR_TRIGGER, False)
    # Allow module to settle
    time.sleep(0.2)
    # Send 10us pulse to trigger
    frontSensor.GPIO.output(FRONT_SENSOR_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(FRONT_SENSOR_TRIGGER, False)
    start = time.time()
    while GPIO.input(FRONT_SENSOR_ECHO) == 0:
        start = time.time()
    while GPIO.input(FRONT_SENSOR_ECHO) == 1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # Multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000 / 2  # distance of both directions so divide by 2
    print ("Front Distance : %.1f" % distance)
    return distance
>>>>>>> ae4a5be47e25296c3641fc4dcbfcb464a57edd5d

def rightobstacle():
    return rightSensor.is_blocked_by_obstacle()

    # # Set trigger to False (Low)
    # GPIO.output(GPIO_TRIGGER_RIGHT, False)
    # # Allow module to settle
    # time.sleep(0.2)
    # # Send 10us pulse to trigger
    # GPIO.output(GPIO_TRIGGER_RIGHT, True)
    # time.sleep(0.00001)
    # GPIO.output(GPIO_TRIGGER_RIGHT, False)
    # start = time.time()
    # while GPIO.input(GPIO_ECHO_RIGHT) == 0:
    #     start = time.time()
    # while GPIO.input(GPIO_ECHO_RIGHT) == 1:
    #     stop = time.time()
    # # Calculate pulse length
    # elapsed = stop - start
    # # Distance pulse travelled in that time is time
    # # Multiplied by the speed of sound (cm/s)
    # distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2
    # print "Right Distance : %.1f" % distance
    # return distance


def leftobstacle():
    return leftSensor.is_blocked_by_obstacle()


# Check front obstacle and turn right if there is an obstacle
def checkanddrivefront():
    while frontobstacle() < 30:
        motor.stop()
        motor.turnRight()
    motor.forward()


# Check right obstacle and turn left if there is an obstacle
def checkanddriveright():
    while rightobstacle() == true:
        motor.stop()
        motor.turnLeft()
    motor.forward()


# Check left obstacle and turn right if there is an obstacle
def checkanddriveleft():
    while leftobstacle() == true:
        motor.stop()
        motor.turnRight()
    motor.forward()


# Avoid obstacles and drive forward
def obstacleavoiddrive():
    motor.forward()
    start = time.time()
    # Drive 5 minutes
    while start > time.time() - 300:  # 300 = 60 seconds * 5
        if frontobstacle() < 30:
            motor.stop()
            checkanddrivefront()
        elif rightobstacle() == true:
            motor.stop()
            checkanddriveright()
        elif leftobstacle() == true:
            motor.stop()
            checkanddriveleft()
    # Clear GPIOs, it will stop motors       
    cleargpios()


def cleargpios():
    print ("clearing GPIO")
<<<<<<< HEAD
    frontSensor.cleanup()
    leftSensor.cleanup()
    rightSensor.cleanup()
=======
    #frontSensor.GPIO.output(FRONT_SENSOR_TRIGGER, False)
    #frontSensor.GPIO.output(FRONT_SENSOR_ECHO, False)
>>>>>>> ae4a5be47e25296c3641fc4dcbfcb464a57edd5d
    # GPIO.output(23, False)
    # GPIO.output(24, False)
    # GPIO.output(16, False)
    # GPIO.output(33, False)
    # GPIO.output(38, False)
    print ("All GPIOs CLEARED")


def main():
    # First clear GPIOs
    cleargpios()
    print ("start driving: ")
    # Start obstacle avoid driving
    obstacleavoiddrive()

if __name__ == "__main__":
    main()

