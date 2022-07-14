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
from micropython import const

class IMU():
    #remove i2c paramater as it is self.cubesat.i2c1

    err_trig = const(100) #this is very low right now so i can see things happen

    def __init__(self, satellite, imu_name, mux_addr=0x70, gyro_addr=0x69,mag_addr=0x30, accel_addr=0x15): #insert optional variables for ignoring devices?
        """
        Init routine
        """
        self.cubesat = satellite
        self.name = imu_name
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

        self.err_cnt = {
            'MUX'   : 0,
            'GYRO0' : 0,
            'GYRO1' : 0,
            'MAG0'  : 0,
            'MAG1'  : 0,
            'ACCEL0': 0,
            'ACCEL1': 0,
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
            print('[INIT][{}][MUX]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][MUX]: {}'.format(self.name, e))
            pass

        #ch0 devices init
        self.mux.set_ch0()
        try:
            self._gyro0 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO0'] = True
            print('[INIT][{}][GYRO0]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}}][GYRO0]: {}'.format(self.name, e))
        try:
            self._mag0 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG0'] = True
            print('[INIT][{}][MAG0]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][MAG0]: {}'.format(self.name, e))
        try:
            self._accel0 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL0'] = True
            print('[INIT][{}][ACCEL0]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][ACCEL0]: {}'.format(self.name, e))
        #ch1 devices init
        self.mux.set_ch1()
        try:
            self._gyro1 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO1'] = True
            print('[INIT][{}][GYRO1]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][GYRO1]: {}'.format(self.name, e))
        try:
            self._mag1 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG1'] = True
            print('[INIT][{}][MAG1]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][MAG1]: {}'.format(self.name, e))
        try:
            self._accel1 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL1'] = True
            print('[INIT][{}][ACCEL1]'.format(self.name))
        except Exception as e:
            self.cubesat.log('[ERROR][{}][ACCEL1]: {}'.format(self.name, e))
        try:
            self.mux.clear()
        except Exception as e:
            self.cubesat.log('[ERROR][{}][MUX]: {}'.format(self.name, e))
        #device default power mode is ON

    """
    Power mode setting
        mode   -- is either "on" or "sleep" right now.
        *argv  -- magical keyword that turns the device names passed to the power state specified
            ex. imu.powermode("off", "gyro1", "mag1", "accel1")

        this needs touch-up --CH
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
                    if self.hardware['GYRO0']:
                        self._gyro0.ON()
                if device is None or device=='mag0':
                    if self.hardware['MAG0']:
                        self._mag0.ON()
                if device is None or device=='accel0':
                    if self.hardware['ACCEL0']:
                        self._accel0.ON()
                #ch1
                self.mux.set_ch1()
                if device is None or device=='gyro1':
                    if self.hardware['GYRO1']:
                        self._gyro1.ON()
                if device is None or device=='mag1':
                    if self.hardware['MAG1']:
                        self._mag1.ON()
                if device is None or device=='accel1':
                    if self.hardware['ACCEL1']:
                        self._accel1.ON()
            elif "min" in mode:
                #ch0 devices
                self.mux.set_ch0()
                if device is None or device=='gyro0':
                    if self.hardware['GYRO0']:
                        self._gyro0.SLEEP()
                if device is None or device=='mag0':
                    if self.hardware['MAG0']:
                        self._mag0.SLEEP()
                if device is None or device=='accel0':
                    if self.hardware['ACCEL0']:
                        self._accel0.SLEEP()
                #ch1
                self.mux.set_ch1()
                if device is None or device=='gyro1':
                    if self.hardware['GYRO1']:
                        self._gyro1.SLEEP()
                if device is None or device=='mag1':
                    if self.hardware['MAG1']:
                        self._mag1.SLEEP()
                if device is None or device=='accel1':
                    if self.hardware['ACCEL1']:
                        self._accel1.SLEEP()
            else:
                print('Invalid Device? ->' + str(device))
            self.mux.clear()
            
            
    """
    returns specified device's reading

    i have a basic error protection going on, imu_task should handle trying to reset devices at x interval if it has errored out (self.err_cnt = b'0xff')


    all of this can probably be written better in less lines

    """

    def _read_device(self, key, ch, device_obj):
        try_again_cnt = 0
        while try_again_cnt <= 2:
            try:
                if ch == 0:
                    self.mux.set_ch0()
                elif ch ==1:
                    self.mux.set_ch1()
                ret = device_obj.read
                try:
                    self.mux.clear()
                except:
                    #increment mux error cntr?
                    pass
                if ret is None:
                    raise Exception('read value is None')
                return ret
            except Exception as e:
                if try_again_cnt < 2:
                    try_again_cnt += 1
                else:
                    print('[WARNING][{}][{}]: {}'.format(self.name, str(key), e))
                    self.err_cnt[key] += 1
                    if self.err_cnt[key] >= self.err_trig:
                        self.cubesat.log('[ERROR][{}][{}][ERROR COUNT EXCEEDED][TURNING DEVICE OFF]'.format(self.name, str(key)))
                        try:
                            self.cubesat.i2c_rst()
                            self.cubesat.i2c_reinit()
                        except:
                            self.cubesat.log('[ERROR][{}][{}][I2C BUS RESET FAILED]]'.format(self.name, str(key)))
                        

    @property
    def gyro0(self):
        if self.hardware['GYRO0']:
            return self._read_device('GYRO0',0, self._gyro0)

    @property
    def gyro1(self):
        if self.hardware['GYRO1']:
            return self._read_device('GYRO1',1, self._gyro1)

    @property
    def mag0(self):
        if self.hardware['MAG0']:
            return self._read_device('MAG0',0, self._mag0)

    @property
    def mag1(self):
        if self.hardware['MAG1']:
            return self._read_device('MAG1',1, self._mag1)

    @property
    def accel0(self):
        if self.hardware['ACCEL0']:
            return self._read_device('ACCEL0',0, self._accel0)

    @property
    def accel1(self):
        if self.hardware['ACCEL1']:
            return self._read_device('ACCEL1',1, self._accel1)

    """
    returns specified device's raw reading
    error checking not implemented, this is really only for debug purposes
    """
    @property
    def gyro0_raw(self):
        if self.hardware['GYRO0']:
            self.mux.set_ch0()
            ret = self._gyro0.read_raw
            self.mux.clear()
            return ret
    
    @property
    def gyro1_raw(self):
        if self.hardware['GYRO1']:
            self.mux.set_ch1()
            ret = self._gyro1.read_raw
            self.mux.clear()
            return ret

    @property
    def mag0_raw(self):
        if self.hardware['MAG0']:
            self.mux.set_ch0()
            ret = self._mag0.read_raw
            self.mux.clear()
            return ret

    @property
    def mag1_raw(self):
        if self.hardware['MAG1']:
            self.mux.set_ch1()
            ret = self._mag1.read_raw
            self.mux.clear()
            return ret
    
    @property
    def accel0_raw(self):
        if self.hardware['ACCEL0']:
            self.mux.set_ch0()
            ret = self._accel0.read_raw
            self.mux.clear()
            return ret
    
    @property
    def accel1_raw(self):
        if self.hardware['ACCEL1']:
            self.mux.set_ch1()
            ret = self._accel1.read_raw
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
