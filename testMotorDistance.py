from motor import Motor
import time

motor = Motor()

print ("Moving forward 1 sec")
motor.forward()
time.sleep(1)
motor.stop()
print ("end going forward")


motor.__del__()
