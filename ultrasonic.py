import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23 #pin 16
ECHO = 24 #pin 18

print "Measuring Distance"

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle" #Sensor needs a bit of time to settle before usage
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0: #A low signal is given when no objects are detected
 pulse_start = time.time() 
 
 while GPIO.input(ECHO)==1: #A high frequency is sent when an object is detected
 pulse_end = time.time()     
 pulse_duration = pulse_end - pulse_start #Measuring Distance
 
 distance = pulse_duration x 17150
 distance = round(distance, 2)
 print "Distance:",distance,"cm" #Prints the distance of the object
 GPIO.cleanup()
 
 
