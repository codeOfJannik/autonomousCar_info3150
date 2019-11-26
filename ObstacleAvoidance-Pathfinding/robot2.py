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
frontSensor = Ultrasonic();
leftSensor = InfraredSensor(21)
rightSensor = InfraredSensor(16)

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
    while (frontobstacle() < 10 or leftobstacle()):
        motor.turnRight()
        time.sleep(1)
	motor.stop()


# Check right obstacle and turn left if there is an obstacle
def checkanddriveright():
    while rightobstacle() or frontobstacle() < 10:
        motor.turnLeft()
        time.sleep(1)
	motor.stop()


# Check left obstacle and turn right if there is an obstacle
def checkanddriveleft():
    while leftobstacle() or frontobstacle() < 10:
        motor.turnRight()
        time.sleep(1)
	motor.stop()


# Avoid obstacles and drive forward
def obstacleavoiddrive():
    motor.forward()
    start = time.time()
    # Drive 5 minutes
    while start > time.time() - 300:  # 300 = 60 seconds * 5
	motor.forward()
        if frontobstacle() < 10:
 	    print("if1")
            motor.stop()
            checkanddrivefront()
        elif rightobstacle() == True:
	    print("if2")
            motor.stop()
            checkanddriveright()
        elif leftobstacle() == True:
	    print("if3")
            motor.stop()
            checkanddriveleft()
    # Clear GPIOs, it will stop motors       
    cleargpios()


def cleargpios():
    print ("clearing GPIO")
    frontSensor.cleanup()
    leftSensor.cleanup()
    rightSensor.cleanup()
    #frontSensor.GPIO.output(FRONT_SENSOR_TRIGGER, False)
    #frontSensor.GPIO.output(FRONT_SENSOR_ECHO, False)
    # GPIO.output(23, False)
    # GPIO.output(24, False)
    # GPIO.output(16, False)
    # GPIO.output(33, False)
    # GPIO.output(38, False)
    print ("All GPIOs CLEARED")


def main():
    print ("start driving: ")
    # Start obstacle avoid driving
    obstacleavoiddrive()
    

if __name__ == "__main__":
    main()

try:
    main()
except KeyboardInterrupt:
    del motor
    del frontSensor
    del leftSensor
    del rightSensor
    print ("Stopped by User")
