"""
`pycubed_IMU.py`
====================================================

CircuitPython lib for a higher level implementation of the IMU blocks on the foras promineo misssion

* Author(s):  C. Hillis

--------------------

"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

import pca9543
import iam20380
import mxc6655
import mmc5983

class imu:

    def __init__(self, i2c_bus, mux_addr, gyro_addr, accel_addr, mag_addr):
        self.mux = pca9543.PCA9543(i2c_bus, mux_addr)
        self.mux.clear()
            #in reality these objects will be used for 2 gyros and 2 accel's and 2 mag's 
            #   but there does not need to be different memory or addr's between them since they will all be operating in parrallel
        gyro = iam23080.IAM23080(i2c_bus, gyro_addr)
        accel = mmxc6655.MMXC6655(i2c_bus, accel_addr)
        mag = mmc5983.MMC5983(i2c_bus, mag_addr)

    @property