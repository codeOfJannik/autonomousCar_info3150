import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import operator
import socket
import os

class Compass:
    SETTINGS_FILE = "RTIMULib"

    def __init__(self):


        s = RTIMU.Settings(self.SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        # offsets
        self.yawoff = 0.0
        self.pitchoff = 0.0
        self.rolloff = 0.0

        # timers
        self.t_print = time.time()
        self.t_damp = time.time()
        self.t_fail = time.time()
        self.t_fail_timer = 0.0
        self.t_shutdown = 0

        # if (not imu.IMUInit()):
        #     hack = time.time()
        #     imu_sentence = "$IIXDR,IMU_FAILED_TO_INITIALIZE*7C"
        #     if (hack - t_print) > 1.0:
        #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #         sock.sendto(imu_sentence, (IMU_IP, IMU_PORT))
        #         t_print = hack
        #         t_shutdown += 1
        #         if t_shutdown > 9:
        #             sys.exit(1)

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.poll_interval = self.imu.IMUGetPollInterval()

        # data variables
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.heading = 0.0
        self.rollrate = 0.0
        self.pitchrate = 0.0
        self.yawrate = 0.0

        # magnetic deviation
        self.magnetic_deviation = 0.0

        # dampening variables
        self.t_one = 0
        self.t_three = 0
        self.roll_total = 0.0
        self.roll_run = [0] * 10
        self.heading_cos_total = 0.0
        self.heading_sin_total = 0.0
        self.heading_cos_run = [0] * 30
        self.heading_sin_run = [0] * 30

    def get_heading(self):
        while True:
            self.hack = time.time()

            # if it's been longer than 5 seconds since last print
            if (self.hack - self.t_damp) > 5.0:

                if (self.hack - self.t_fail) > 1.0:
                    self.t_one = 0
                    self.t_three = 0
                    self.roll_total = 0.0
                    self.roll_run = [0] * 10
                    self.heading_cos_total = 0.0
                    self.heading_sin_total = 0.0
                    self.heading_cos_run = [0] * 30
                    self.heading_sin_run = [0] * 30
                    self.t_fail_timer += 1
                    self.imu_sentence = "IIXDR,IMU_FAIL," + str(round(self.t_fail_timer / 60, 1))
                    self.cs = format(reduce(operator.xor, map(ord, self.imu_sentence), 0), 'X')
                    if len(self.cs) == 1:
                        self.cs = "0" + self.cs
                    self.imu_sentence = "$" + self.imu_sentence + "*" + self.cs
                    self.t_fail = self.hack
                    self.t_shutdown += 1

            if self.imu.IMURead():
                self.data = self.imu.getIMUData()
                self.fusionPose = data["fusionPose"]
                Gyro = data["gyro"]
                t_fail_timer = 0.0

                if (self.hack - self.t_damp) > .1:
                    self.roll = round(math.degrees(fusionPose[0]) - self.rolloff, 1)
                    self.pitch = round(math.degrees(fusionPose[1]) - self.pitchoff, 1)
                    self.yaw = round(math.degrees(fusionPose[2]) - self.yawoff, 1)
                    self.rollrate = round(math.degrees(Gyro[0]), 1)
                    self.pitchrate = round(math.degrees(Gyro[1]), 1)
                    self.yawrate = round(math.degrees(Gyro[2]), 1)
                    if self.yaw < 0.1:
                        self.yaw = self.yaw + 360
                    if self.yaw > 360:
                        self.yaw = self.yaw - 360

                    # Dampening functions
                    self.roll_total = self.roll_total - self.roll_run[t_one]
                    self.roll_run[self.t_one] = self.roll
                    self.roll_total = self.roll_total + self.roll_run[self.t_one]
                    self.roll = round(self.roll_total / 10, 1)
                    self.heading_cos_total = self.heading_cos_total - heading_cos_run[self.t_three]
                    self.heading_sin_total = self.heading_sin_total - heading_sin_run[self.t_three]
                    self.heading_cos_run[self.t_three] = math.cos(math.radians(self.yaw))
                    self.heading_sin_run[self.t_three] = math.sin(math.radians(self.yaw))
                    self.heading_cos_total = self.heading_cos_total + self.heading_cos_run[t_three]
                    self.heading_sin_total = self.heading_sin_total + self.heading_sin_run[t_three]
                    self.yaw = round(math.degrees(math.atan2(self.heading_sin_total / 30, self.heading_cos_total / 30)), 1)
                    if self.yaw < 0.1:
                        self.yaw = self.yaw + 360.0

                    # yaw is magnetic heading, convert to true heading
                    self.heading = self.yaw - self.magnetic_deviation
                    if self.heading < 0.1:
                        self.heading = self.heading + 360
                    if self.heading > 360:
                        self.heading = self.heading - 360

                    return self.heading

                time.sleep(self.poll_interval * 1.0 / 1000.0)
