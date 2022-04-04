"""
`pycubed_IMU.py`
====================================================

CircuitPython lib for a higher level implementation of the IMU block on the foras promineo mainboard and payload

* Author(s):  C. Hillis

====================================================

IMU Structure

I2C bus    _____   ch0    _____
==========| MUX |-----T--|Gyro0|
           ‾‾†‾‾      |   ‾‾‾‾‾
           c |        |   _____________
           h |        ⊦--|Magnetometer0|
           1 |        |   ‾‾‾‾‾‾‾‾‾‾‾‾‾
             |        |   ______
             |        L--|Accel0|
             |            ‾‾‾‾‾‾
             |             _____
             L--------T---|Gyro1|
                      |    ‾‾‾‾‾
                      |   _____________
                      ⊦--|Magnetometer1|
                      |   ‾‾‾‾‾‾‾‾‾‾‾‾‾
                      |   ______
                      L--|Accel1|
                          ‾‾‾‾‾‾
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

import pca9543
import iam20380
import mxc6655
import mmc5983

class imu():

    def __init__(self, i2c, mux_addr, gyro_addr=0x69,mag_addr=0x70, accel_addr=0x16): #insert optional variables for ignoring devices?
        """
        Init routine
        """

        #saving variables passed to the class
        self.i2c = i2c
        self.mux_addr = mux_addr
        self.gyro_addr = gyro_addr
        self.accel_addr = accel_addr

        # table that stores whether or not a device is active or not
        self.hardware = {
            'MUX'   : False,
            'GYRO0' : False,
            'GYRO1' : False,
            'MAG0'  : False,
            'MAG1'  : False,
            'ACCEL0': False,
            'ACCEL1': False,
        }

        #initialize mux
        try:
            self.mux = pca9543.PCA9543(i2c, mux_addr)
            self.mux.set_ch0()
        except Exception as e:
            pass

        """
        in reality these will be used for 2 gyros, 2 mag's and 1 accel 
                but there does not need to be different memory or addr's between; them pca9543 mux's the i2c lines and the classes dont really save any independent data
                how to pass to this class that init failed?
                    maybe have __init's of these libs return none on init if they failed?
        """
        self.gyro = iam20380.IAM20380(i2c, gyro_addr) 
        self.accel = mxc6655.MXC6655(i2c, accel_addr)
        self.mag = mmc5983.MMC5983(i2c, mag_addr)