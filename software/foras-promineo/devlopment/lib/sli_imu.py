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
        super.__init__(satellite)

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
        '''
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
        '''
        #initialize mux
        try:
            self.mux = pca9543.PCA9543(self.cubesat.i2c1, mux_addr)
            self.mux.set_ch0()
            self.mux.clear()
            self.hardware['MUX'] = True
        except Exception as e:
            pass

        """
        in reality these will be used for 2 gyros, 2 mag's and 1 accel 
                but there does not need to be different memory or addr's between; them pca9543 mux's the i2c lines and the classes dont really save any independent data
        if init of a lower device fails the class will error out and the try except will catch it.
        """
        
        #ch0 devices init
        self.mux.set_ch0()
        try:
            self.gyro0 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO0'] = True
            print('[INIT][IMU][GYRO0]')
        except Exception as e:
            self.log('[ERROR][IMU][GYRO0]' + str(e))
        try:
            self.mag0 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG0'] = True
            print('[INIT][IMU][MAG0]')
        except Exception as e:
            self.log('[ERROR][IMU][MAG0]' + str(e))
        try:
            self.accel0 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL0'] = True
            print('[INIT][IMU][ACCEL0]')
        except Exception as e:
            self.log('[ERROR][IMU][ACCEL0]' + str(e))
        #ch1 devices init
        self.mux.set_ch1()
        try:
            self.gyro1 = iam20380.IAM20380(self.cubesat.i2c1, gyro_addr)
            self.hardware['GYRO1'] = True
            print('[INIT][IMU][GYRO1]')
        except Exception as e:
            self.log('[ERROR][IMU][GYRO1]' + str(e))
        try:
            self.mag1 = mmc5983.MMC5983(self.cubesat.i2c1, mag_addr)
            self.hardware['MAG1'] = True
            print('[INIT][IMU][MAG1]')
        except Exception as e:
            self.log('[ERROR][IMU][MAG1]' + str(e))
        try: #accel 1 is DNP, so this may toss an error but is NBD
            self.accel1 = mxc6655.MXC6655(self.cubesat.i2c1, accel_addr)
            self.hardware['ACCEL1'] = True
            print('[INIT][IMU][ACCEL1]')
        except Exception as e:
            self.log('[ERROR][IMU][ACCEL1]' + str(e))

        #device default power mode is ON

    """
    Re-initializes device passed
    this function MUST be called in a try-except clause if the init fails!!
    it is also up to the user to correctly update the self.hardware dict!!
            this function purposely does not accept multiple args!
    """
    def reinit(self, dev):
        dev=dev.lower()
        if   dev=='mux':
            self.mux.__init__()
        elif dev=='gyro0':
            self.mux.set_ch0()
            self.gyro0.__init__()
        elif dev=='gyro1':
            self.mux.set_ch1()
            self.gyro1.__init__()
        elif dev=='mag0':
            self.mux.set_ch0()
            self.mag0.__init__()
        elif dev=='mag1':
            self.mux.set_ch1()
            self.mag1.__init__()
        elif dev=='accel0':
            self.mux.set_ch0()
            self.accel0.__init__()
        elif dev=='accel1':
            self.mux.set_ch1()
            self.accel1.__init__()
        else:
            print('Invalid Device? ->' + str(dev))

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
        #make sure this works if devices is not passed to the function
        for device in devices:
            if device is not None: device=device.lower()
            if mode=="on":
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
            elif mode=="sleep":
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
            
    """
    returns specified device's reading
        if device is False in device table, it will return none.
    see read_temp for a aquiring temp of specific devices
    """
    @property
    def gyro0(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['GRYO0']:
            self.mux.set_ch0()
            return self.gyro0.read() #dps
    
    @property
    def gyro1(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['GRYO1']:
            self.mux.set_ch1()
            return self.gyro1.read() #dps
                  
    @property
    def mag0(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['MAG0']:
            self.mux.set_ch0()
            return self.mag0.read() #mG CHANGE TO uT

    @property
    def mag1(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['MAG1']:
            self.mux.set_ch1()
            return self.mag1.read() #mG
    
    @property
    def accel0(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['ACCEL0']:
            self.mux.set_ch0()
            return self.accel0.read() #g CHANGE TO m/s^2
    
    @property
    def accel1(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['ACCEL1']:
            self.mux.set_ch1()
            return self.accel1.read() #

    """
    returns specified device's temperature reading
        if device is False in device table, it will return none.
        evaluate each device and use as needed, as the temp sensor for the IAM20380(gyro) is slightly off no matter what I try 
        -- and it isn't worth it to fine tune the paramater when I have 5 more temp sensors in the same area
    """
    @property
    def gyro0_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['GRYO0']:
            self.mux.set_ch0()
            return self.gyro0.temp()
    
    @property
    def gyro1_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['GRYO1']:
            self.mux.set_ch1()
            return self.gyro1.temp()
                  
    @property
    def mag0_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['MAG0']:
            self.mux.set_ch0()
            return self.mag0.temp()

    @property
    def mag1_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['MAG1']:
            self.mux.set_ch1()
            return self.mag1.temp()
    
    @property
    def accel0_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['ACCEL0']:
            self.mux.set_ch0()
            return self.accel0.temp()
    
    @property
    def accel1_t(self):
        #if self.cubesat.simulation:
        if self.cubesat.hardware['IMU'] and self.hardware['ACCEL1']:
            self.mux.set_ch1()
            return self.accel1.temp()
