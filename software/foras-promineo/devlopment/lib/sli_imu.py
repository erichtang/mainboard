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

import pca9543
import iam20380
import mxc6655
import mmc5983

class IMU():
    #remove i2c paramater as it is self.cubesat.i2c1
    def __init__(self, satellite, mux_addr=0x70, gyro_addr=0x69,mag_addr=0x30, accel_addr=0x15): #insert optional variables for ignoring devices?
        """
        Init routine
        """
        self.cubesat = satellite

        #saving variables passed to the class
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

        """
        #dict that can store offset values the user writes to it. not really used now.
        #maybe implement with the read function, and have a raw (scaled) function?
        # need to play with sensor offsets before I start messing with this.
        self.calibration = {
            'GYRO0'     : [0,0,0],
            'GYRO1'     : [0,0,0],
            'MAG0'      : [0,0,0],
            'MAG1'      : [0,0,0],
            'ACCEL0'    : [0,0,0],
            'ACCEL1'    : [0,0,0],
        }
        """
        #initialize mux
        try:
            self.mux = pca9543.PCA9543(self.cubesat.i2c1, mux_addr)
            self.mux.set_ch0()
            self.mux.clear()
            self.hardware['MUX'] = True
            print('[INIT][IMU][MUX]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][MUX]: ' + str(e))
            pass

        #ch0 devices init
        self.mux.set_ch0()
        try:
            self.gyro0 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO0'] = True
            print('[INIT][IMU][GYRO0]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][GYRO0]: ' + str(e))
        try:
            self.mag0 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG0'] = True
            print('[INIT][IMU][MAG0]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][MAG0]: ' + str(e))
        try:
            self.accel0 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL0'] = True
            print('[INIT][IMU][ACCEL0]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][ACCEL0]: ' + str(e))
        #ch1 devices init
        self.mux.set_ch1()
        try:
            self.gyro1 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO1'] = True
            print('[INIT][IMU][GYRO1]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][GYRO1]: ' + str(e))
        try:
            self.mag1 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG1'] = True
            print('[INIT][IMU][MAG1]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][MAG1]: ' + str(e))
        try: #accel 1 is DNP, so this may toss an error but is NBD
            self.accel1 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL1'] = True
            print('[INIT][IMU][ACCEL1]')
        except Exception as e:
            self.cubesat.log('[ERROR][IMU][ACCEL1]: ' + str(e))
        self.mux.clear()
        #device default power mode is ON

    """
    Power mode setting
        mode   -- is either "on" or "sleep" right now.
        *argv  -- magical keyword that turns the device names passed to the power state specified
            ex. imu.powermode("off", "gyro1", "mag1", "accel1")
    """
    def powermode(self, mode, *devices):
        mode=mode.lower()
        for device in devices:
            if device is not None:     
                device = device.lower()
        for device in devices:
            if device is not None: device=device.lower()
            if "norm" in mode:
                #ch0 devices
                self.mux.set_ch0()
                if device is None or device=='gyro0':
                    if self.hardware['GYRO0'] == True:
                        self.gyro0.ON()
                if device is None or device=='mag0':
                    if self.hardware['MAG0'] == True:
                        self.mag0.ON()
                if device is None or device=='accel0':
                    if self.hardware['ACCEL0'] == True:
                        self.accel0.ON()
                #ch1
                self.mux.set_ch1()
                if device is None or device=='gyro1':
                    if self.hardware['GYRO1'] == True:
                        self.gyro1.ON()
                if device is None or device=='mag1':
                    if self.hardware['MAG1'] == True:
                        self.mag1.ON()
                if device is None or device=='accel1':
                    if self.hardware['ACCEL1'] == True:
                        self.accel1.ON()
            elif "min" in mode:
                #ch0 devices
                self.mux.set_ch0()
                if device is None or device=='gyro0':
                    if self.hardware['GYRO0'] == True:
                        self.gyro0.SLEEP()
                if device is None or device=='mag0':
                    if self.hardware['MAG0'] == True:
                        self.mag0.SLEEP()
                if device is None or device=='accel0':
                    if self.hardware['ACCEL0'] == True:
                        self.accel0.SLEEP()
                #ch1
                self.mux.set_ch1()
                if device is None or device=='gyro1':
                    if self.hardware['GYRO1'] == True:
                        self.gyro1.SLEEP()
                if device is None or device=='mag1':
                    if self.hardware['MAG1'] == True:
                        self.mag1.SLEEP()
                if device is None or device=='accel1':
                    if self.hardware['ACCEL1'] == True:
                        self.accel1.SLEEP()
            else:
                print('Invalid Device? ->' + str(device))
            self.mux.clear()
            
            
    """
    returns specified device's reading
    """
    @property
    def gyro0(self):
        if self.hardware['GYRO0']:
            self.mux.set_ch0()
            ret =  self.gyro0.gyro
            self.mux.clear()
            return ret
    
    @property
    def gyro1(self):
        if self.hardware['GYRO1']:
            self.mux.set_ch1()
            ret = self.gyro1.gyro
            self.mux.clear()
            return ret
                  
    @property
    def mag0(self):
        if self.hardware['MAG0']:
            self.mux.set_ch0()
            ret = self.mag0.mag
            self.mux.clear()
            return ret

    @property
    def mag1(self):
        if self.hardware['MAG1']:
            self.mux.set_ch1()
            ret = self.mag1.mag
            self.mux.clear()
            return ret
    
    @property
    def accel0(self):
        if self.hardware['ACCEL0']:
            self.mux.set_ch0()
            ret = self.accel0.accel
            self.mux.clear()
            return ret

    @property
    def accel1(self):
        if self.hardware['ACCEL1']:
            self.mux.set_ch1()
            ret = self.accel1.accel
            self.mux.clear()
            return ret

    """
    returns specified device's raw reading
    """
    @property
    def gyro0_raw(self):
        if self.hardware['GYRO0']:
            self.mux.set_ch0()
            ret = self.gyro0.gyro_raw
            self.mux.clear()
            return ret
    
    @property
    def gyro1_raw(self):
        if self.hardware['GYRO1']:
            self.mux.set_ch1()
            ret = self.gyro1.gyro_raw
            self.mux.clear()
            return ret

    @property
    def mag0_raw(self):
        if self.hardware['MAG0']:
            self.mux.set_ch0()
            ret = self.mag0.mag_raw
            self.mux.clear()
            return ret

    @property
    def mag1_raw(self):
        if self.hardware['MAG1']:
            self.mux.set_ch1()
            ret = self.mag1.mag_raw
            self.mux.clear()
            return ret
    
    @property
    def accel0_raw(self):
        if self.hardware['ACCEL0']:
            self.mux.set_ch0()
            ret = self.accel0.accel_raw
            self.mux.clear()
            return ret
    
    @property
    def accel1_raw(self):
        if self.hardware['ACCEL1']:
            self.mux.set_ch1()
            ret = self.accel1.accel_raw
            self.mux.clear()
            return ret

    """
    returns specified device's temperature reading
        evaluate each device and use as needed, as the temp sensor for the IAM20380(gyro) is slightly off no matter what I try 
    """
    @property
    def gyro0_t(self):
        if self.hardware['GYRO0']:
            self.mux.set_ch0()
            ret = self.gyro0.temp
            self.mux.clear()
            return ret
    
    @property
    def gyro1_t(self):
        if self.hardware['GYRO1']:
            self.mux.set_ch1()
            ret = self.gyro1.temp
            self.mux.clear()
            return ret
                  
    @property
    def mag0_t(self):
        if self.hardware['MAG0']:
            self.mux.set_ch0()
            ret = self.mag0.temp
            self.mux.clear()
            return ret

    @property
    def mag1_t(self):
        if self.hardware['MAG1']:
            self.mux.set_ch1()
            ret = self.mag1.temp
            self.mux.clear()
            return ret
    
    @property
    def accel0_t(self):
        if self.hardware['ACCEL0']:
            self.mux.set_ch0()
            ret = self.accel0.temp
            self.mux.clear()
            return ret
    
    @property
    def accel1_t(self):
        if self.hardware['ACCEL1']:
            self.mux.set_ch1()
            ret = self.accel1.temp
            self.mux.clear()
            return ret
