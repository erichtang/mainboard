"""
`pycubed_IMU.py`
====================================================

CircuitPython lib for a higher level implementation of the IMU block on the foras promineo misssion



* Author(s):  C. Hillis

--------------------

"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

import pca9543
import iam20380
import mxc6655
import mmc5983

class _buffer:
    def __init__(self, depth):
        self.buffer = [float] * depth

class IMU:

    def __init__(self, i2c_bus, mux_addr, gyro_addr, accel_addr, mag_addr, buff_len):

        self.buff_len = buff_len # maybe add code to make this changeable?

        self.mux = pca9543.PCA9543(i2c_bus, mux_addr)
        self.mux.set_ch0()
        """
        in reality these will be used for 2 gyros, 2 mag's and 1 accel 
                but there does not need to be different memory or addr's between; them pca9543 mux's the i2c lines and the classes dont really save any independent data
                how to pass to this class that init failed?
                    maybe have __init's of these libs return none on init if they failed?
        """
        self.gyro = iam20380.IAM20380(i2c_bus, gyro_addr) 
        self.accel = mxc6655.MXC6655(i2c_bus, accel_addr)
        self.mag = mmc5983.MMC5983(i2c_bus, mag_addr)

        """
        initialize data structure
            saving buff_length # of measurements, 
            for 4 measurements (x, y, z, temp), 
            2 devices for each type of measurement ( i.e. 2 gyros)(except accel), 
            and three types of devices (gyro, mag, and accel)
        TLDR; ex. .foo[self._buffer_i][1][2] = most recent, from ch1, y axis
            reading the buffer from a higher-up program will need to call .gyro(), .mag(), or .accel(), or .temp()
        """
        self.buffer_i   = 0 # buffer iterator for simple implementation
        self._gyro_b     = [[[float] * 3] * 2] * self.buff_len
        self._mag_b      = [[[float] * 3] * 2] * self.buff_len
        self._accel_b    = [[float] * 3] * self.buff_len # only accel 1 (on ch1) is populated
        self._temp_b     = [[float] * 5] * self.buff_len # each devices has a temperature measurement, we could either avg them all or just take one.

        #device health should be handled by the lower libraries, i think once we init we are fine to just take readings and change operating modes
        self.ON()
        self.read()
    
    """
    --------------------------------------------------------------
    turns on all devices so most recent data is ready to be read
        if turning on from OFF, longest device startup is 35ms
    """
    def ON(self):
        # turn all ch1 devices on
        # turn all ch2 devices on
        # take ch1 measurements
        # take ch2 measurements
        pass

    """
    --------------------------------------------------------------
    turns all devices to a low power state
    """
    def OFF(self):
        #set ch1 to off
        # set ch2 to off
        pass

    """
    --------------------------------------------------------------
    updates the buffers, each buffer will have to be called separtely to read them
        ADD NONE CATCHERS TO OUTPUTS BEFORE THEY ARE ADJUSTED in device libs
    """
    
    def read(self):
        #iteration of buffer index first so references can be made to most recent data easily
        if(self.buffer_i==(self.buff_len-1)):
            self.buffer_i = 0
        else:
            self.buffer_i += 1
        #ch0
        self.mux.set_ch0()
        #taking meas's
        self._gyro_b[self.buffer_i][0] = self.gyro.read()
        self._mag_b[self.buffer_i][0] = self.mag.read()
        self._accel_b[self.buffer_i] = self.accel.read()

        self._temp_b[self.buffer_i][0] = self.gyro.temp()
        self._temp_b[self.buffer_i][1] = self.mag.temp()
        self._temp_b[self.buffer_i][2] = self.accel.temp()
        #ch1
        self.mux.set_ch1()
        self._gyro_b[self.buffer_i][1] = self.gyro.read()
        self._mag_b[self.buffer_i][1] = self.mag.read()

        self._temp_b[self.buffer_i][3] = self.gyro.temp()
        self._temp_b[self.buffer_i][4] = self.mag.temp()

        self.mux.clear()
    
    """
    --------------------------------------------------------------
    functions that return whole buffer for selected type of measurement
        must call .read() for most recent data
    """
    @property
    def gyro_data(self):
        return(self._gyro_b)
    @property
    def mag_data(self):
        return(self._mag_b)
    @property
    def accel_data(self):
        return(self._accel_b)
    @property
    def temp_data(self):
        return(self._temp_b)

    """
    --------------------------------------------------------------
    quick check functions for reading only one value on the fly (useful if you dont want to handle the *slightly* confusing structuring of the data above)
    must call .read() for most recent data
        returns list = [float, float, float] data of measurement 
        may list object may be type'd None if no data was read
    """
    @property
    def qc_gyro(self):
        return(self._gyro_b[self.buffer_i][0])
    @property
    def qc_mag(self):
        return(self._mag_b[self.buffer_i][0])
    @property
    def qc_accel(self):
        return(self._accel_b[self.buffer_i])
    @property
    def qc_temp(self):
        return(self._temp_b[self.buffer_i][1]) # not taking temp from gyro rn that is a little off.

    # min, max, avg, and largest delta calculations maybe?