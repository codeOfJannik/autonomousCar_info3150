import RPi.GPIO as gpio
import time

class InfraredSensor:

	def __init__(self, pin):
		gpio.setmode(gpio.BCM)
		self.SENSORPIN = pin
		gpio.setup(self.SENSORPIN, gpio.IN)

	def is_blocked_by_obstacle(self):
		return not gpio.input(self.SENSORPIN)
