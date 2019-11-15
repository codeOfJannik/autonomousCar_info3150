from motor import Motor
import time

motor = Motor()

print ("start going forward")
motor.forward()
time.sleep(2)
motor.stop()
print ("end going forward")

time.sleep(1)

print ("start going backward")
motor.backward()
time.sleep(2)
motor.stop()
print ("end going backward")

time.sleep(1)

print ("start turning left")
motor.turnLeft()
time.sleep(2)
motor.stop()
print ("end turning left")

time.sleep(1)

print ("start turning right")
motor.turnRight()
time.sleep(2)
motor.stop()
print ("end turning right")

motor.__del__()