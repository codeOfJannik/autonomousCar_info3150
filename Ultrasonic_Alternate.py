import RPi.GPIO as GPIO                                                 # Import the GPIO module as 'GPIO'

import time

GPIO.setmode (GPIO.BCM)                                                 # Set the GPIO mode to BCM numbering
output_ports = [4]                                                      # Define the GPIO output port numbers
input_ports = [17]                                                      # Define the GPIO input port numbers

trig=4                                                                  # set trigger port
echo=17                                                                 # set echo port

# HC-SR04 ULTRASONIC DISTANCE SENSOR                                *
# *******************************************************************
# * Unfortunately, the HC-SR04 suffers from some inherent built-in  *
# * flaws, particularly if the reflected sound waves bounce off     *
# * objects at a distance and/or at oblique angles.  This results   *
# * in very erratic signals being generated on the 'Echo' pin.      *
# * This function filters out most erratic events. If a valid       *
# * measurement was detected, the distance is given in cm units.    *
# * If a measurement error was detected, a negative error code is   *
# * returned.                                                       *
# *******************************************************************

def get_distance():
    if GPIO.input (echo):                                               # If the 'Echo' pin is already high
        return (-1)                                                     # then exit with error code

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (trig,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.03)                                                   # least 30mS 

    GPIO.output (trig,True)                                             # Turn on the 'Trig' pin for 10us
    time.sleep (1e-5)
                
    GPIO.output (trig,False)                                            # Turn off the 'Trig' pin
    time.sleep (1e-5)
    
    if GPIO.input (echo):
        distance = -2                                                   # If a sensor error has occurred
        return (distance)                                               # then exit with error code
    
    time1, time2 = time.time(), time.time()                             #init times
    
    while not GPIO.input (echo):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = -3                                              # then set 'distance' to 100
            break                                                         # and break out of the loop
        
    if distance == -3:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)
    
    time2 = time.time() 
    while GPIO.input (echo):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if (time2 - time1 > 0.02):                                      # If the 'Echo' pin doesn't go low after 20mS
            distance = -4                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop
    
    if (time2 - time1 < 3.0e-5):                                        # If the 'Echo' pin went low too fast
        distance = -5
        
    if distance < 0:                                                    # If a sensor error has occurred
        return (distance)                                               # then exit with error code
        
                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)
                                                                        
    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    return (distance)                                                   # Exit with the distance in centimetres


for bit in output_ports:                                                # Set up the six output bits
    GPIO.setup (bit,GPIO.OUT)
    GPIO.output (bit,False)                                             # Initially turn them all off
    
for bit in input_ports:                                                 # Set up the six input bits
    GPIO.setup (bit,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)              # Set the inputs as normally low

while True:
    distance = get_distance()
    if distance >0:
        print(distance)
