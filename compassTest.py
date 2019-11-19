from navigationSensor import NavigationSensor

navigationSensor = NavigationSensor()

try:
    while True:
        bearTo = navigationSensor.get_compass_value()
        print(str(bearTo))
except KeyboardInterrupt:
    print("Quit")