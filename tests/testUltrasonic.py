from ultrasonic import Ultrasonic
import time
import sys
sys.path.insert(1, '../')

sensor = Ultrasonic()

while True:
    try:
        distance = sensor.sense()
        print ("Distance:",distance,"cm")
        time.sleep(0.5)
    except KeyboardInterrupt:
        sensor.end()
