from navigationSensor import NavigationSensor
import time

navigationSensor = NavigationSensor()

try:
    while True:
        bearTo = navigationSensor.get_compass_value()
        print(str(bearTo))
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Quit")