import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

class NavigationSensor:

    __SETTINGS_FILE = "RTIMULib"

    def __init__(self):
        print("Using settings file " + self.__SETTINGS_FILE + ".ini")
        if not os.path.exists(self.__SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        s = RTIMU.Settings(self.__SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        print("IMU Name: " + self.imu.IMUName())

        if not self.imu.IMUInit():
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded")

        # this is a good time to set any fusion parameters

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.poll_interval = self.imu.IMUGetPollInterval()

    def __convert_fusion_value_to_positive_bearing(self, fusionValue):
        if fusionValue < 0:
            return 360 + fusionValue
        return fusionValue

    def get_compass_value(self):
        while True:
            if self.imu.IMURead():
                data = self.imu.getIMUData()
                fusionPose = data["fusionPose"]
                bearTo = math.degrees(fusionPose[2])
                return self.__convert_fusion_value_to_positive_bearing(bearTo)
            time.sleep(self.poll_interval * 1.0 / 1000.0)

