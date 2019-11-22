import sys, getopt
from thread import start_new_thread

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import operator
import socket
import os

class Compass:

    __SETTINGS_FILE = "RTIMULib"

    roll = 0.0
    pitch = 0.0
    yaw = 0.0
    heading = 0.0
    rollrate = 0.0
    pitchrate = 0.0
    yawrate = 0.0
    magnetic_deviation = 0.0

    t_one = 0
    t_three = 0
    roll_total = 0.0
    roll_run = [0] * 10
    heading_cos_total = 0.0
    heading_sin_total = 0.0
    heading_cos_run = [0] * 30
    heading_sin_run = [0] * 30

    def __init__(self):
        s = RTIMU.Settings(self.__SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.poll_interval = self.imu.IMUGetPollInterval()

    def measurment_function(self):
        while True:

            if self.imu.IMURead():
                data = self.imu.getIMUData()
                fusionPose = data["fusionPose"]
                Gyro = data["gyro"]

                self.roll = round(math.degrees(fusionPose[0]), 1)
                self.pitch = round(math.degrees(fusionPose[1]), 1)
                self.yaw = round(math.degrees(fusionPose[2]), 1)
                self.rollrate = round(math.degrees(Gyro[0]), 1)
                self.pitchrate = round(math.degrees(Gyro[1]), 1)
                self.yawrate = round(math.degrees(Gyro[2]), 1)
                if self.yaw < 0.1:
                    self.yaw = self.yaw + 360
                if self.yaw > 360:
                    self.yaw = self.yaw - 360

                # Dampening functions
                self.roll_total = self.roll_total - self.roll_run[self.t_one]
                self.roll_run[self.t_one] = self.roll
                self.roll_total = self.roll_total + self.roll_run[self.t_one]
                self.roll = round(self.roll_total / 10, 1)
                self.heading_cos_total = self.heading_cos_total - self.heading_cos_run[self.t_three]
                self.heading_sin_total = self.heading_sin_total - self.heading_sin_run[self.t_three]
                self.heading_cos_run[self.t_three] = math.cos(math.radians(self.yaw))
                self.heading_sin_run[self.t_three] = math.sin(math.radians(self.yaw))
                self.heading_cos_total = self.heading_cos_total + self.heading_cos_run[self.t_three]
                self.heading_sin_total = self.heading_sin_total + self.heading_sin_run[self.t_three]
                self.yaw = round(math.degrees(math.atan2(self.heading_sin_total / 30, self.heading_cos_total / 30)),
                                 1)
                if self.yaw < 0.1:
                    self.yaw = self.yaw + 360.0

                # yaw is magnetic heading, convert to true heading
                self.heading = self.yaw - self.magnetic_deviation
                if self.heading < 0.1:
                    self.heading = self.heading + 360
                if self.heading > 360:
                    self.heading = self.heading - 360

            time.sleep(poll_interval * 1.0 / 1000.0)

    def start_measurment(self):
        start_new_thread(self.measurment_function())

