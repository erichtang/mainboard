# mmc5983.py
#
# circuitpython driver lib for mmc5983 magnetometer
#
# C. Hillis 3/22

from time import sleep
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

# Register Map
XOUT0               = const(0x00) #Xout [17:10]
XOUT1               = const(0x01) #Xout [9:2]
YOUT0               = const(0x02)
YOUT1               = const(0x03)
ZOUT0               = const(0x04)
ZOUT1               = const(0x05)
XYZOUT              = const(0x06) #Xout[1:0], Yout[1:0], Zout[1:0]
TOUT                = const(0x07)
STATUS              = const(0x08)
INTERNAL_CONTROL_0  = const(0x09)
INTERNAL_CONTROL_1  = const(0x09)
INTERNAL_CONTROL_2  = const(0x09)
INTERNAL_CONTROL_3  = const(0x09)
PRODUCT_ID_1        = const(0x0A)

class MMC5983:

    # Class Variables (NOT ALL REGISTERS AND FUNCTIONS ARE IMPLEMENTED)
    _xout0 = UnaryStruct(XOUT0, "<B")
    _xout1 = UnaryStruct(XOUT1, "<B")
    _yout0 = UnaryStruct(YOUT0, "<B")
    _yout1 = UnaryStruct(YOUT1, "<B")
    _zout0 = UnaryStruct(ZOUT0, "<B")
    _zout1 = UnaryStruct(ZOUT1, "<B")
    _xyzout = UnaryStruct(XYZOUT, "<B")
    _tout = UnaryStruct(TOUT, "<B")
    _meas_m_done = ROBit(STATUS, 0)
    _meas_t_done = ROBit(STATUS, 1)
    _tm_m = RWBit(INTERNAL_CONTROL_0, 0)
    _tm_t = RWBit(INTERNAL_CONTROL_0, 1)
    _auto_sr_en = RWBit(INTERNAL_CONTROL_0, 5)
    _bw = RWBits(2, INTERNAL_CONTROL_1, 0)
    _reset = RWBit(INTERNAL_CONTROL_1, 7)
    _cm_freq = RWBits(3, INTERNAL_CONTROL_2, 0)
    _cmm_en = RWBit(INTERNAL_CONTROL_2, 3)
    _prd_set = RWBits(3, INTERNAL_CONTROL_2, 4)
    _en_prd_set = RWBit(INTERNAL_CONTROL_2, 7)
    _st_en_p = RWBit(INTERNAL_CONTROL_3, 1)
    _st_en_n = RWBit(INTERNAL_CONTROL_3, 2)
    _p_id = ROBits(4, PRODUCT_ID_1, 4)

    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        test = self._p_id
        if not test == 3 : print("[ERROR][IAM20380][BAD P_ID VALUE]")
        self.sleep()

    def high_preformance(self):
        print()

    def low_power(self):
        print()

    def sleep(self):
        print()

    def reset(self): #device startup time is 10ms, but how to tell device to do something else for 10ms before coming back and reading? (since this is a very low level lib)
        self._reset = True
        sleep(.01)

    @property
    def x_raw(self):
        x_raw = (self._xout0 << 10) + (self._xout1 << 2) + (self._xyzout >> 6)
        return(x_raw)
    
    @property
    def y_raw(self):
        y_raw = (self._yout0 << 10) + (self._yout1 << 2) + ((self._xyzout & 0x30) >> 4)
        return(y_raw)
    
    @property
    def z_raw(self):
        z_raw = (self._zout0 << 10) + (self._zout1 << 2) + ((self._xyzout & 0xC) >> 2)
        return(z_raw)
    
    @property
    def x(self):
        x = self._adj(self.x_raw)
        return(x)
    
    @property
    def y(self):
        y = self._adj(self.y_raw)
        return(y)
    
    @property
    def z(self):
        z = self._adj(self.z_raw)
        return(z)

    def _adj(value): # adjusts raw values to mG, sensor default sensitivity is 16384 counts/G, 1G/1000mG, are these signed???
        adj = (value/16.384)

    @property
    def t_raw(self):
        t_raw = self._tout
        return t_raw
    
    @property
    def t(self): #datasheet says 0.8degC per cnt, -75degC offset
        t = (self.t_raw * 0.8) - 75

    @property
    def auto_sr(self):
        return(self._auto_sr_en) # 1 for on 0 for off, not really sure what the benefits of this are.
    @auto_sr.setter
    def auto_sr(self, value):
        self._auto_sr_en = value
    
    @property
    def bw(self):
        return(self._bw)
    @bw.setter
    def bw(self, value):
        self._bw = value

    @property
    def cm_freq(self):
        return(self._cm_freq)
    @cm_freq.setter
    def cm_freq(self, value):
        self._cm_freq = value

    @property
    def cmm_en(self):
        return(self._cmm_en)
    @cmm_en.setter
    def cmm_en(self, value):
        self._cmm_en = value

    @property
    def prd_set(self):
        return(self._prd_set)
    @prd_set.setter
    def prd_set(self, value):
        self._prd_set = value

    @property
    def en_prd_set(self):
        return(self._en_prd_set)
    @en_prd_set.setter
    def en_prd_set(self, value):
        self._en_prd_set = value

    #def selftest(self): #self tests magnetic sensors for saturation, not impllemented