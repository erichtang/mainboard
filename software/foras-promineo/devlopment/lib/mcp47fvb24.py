"""
 mcp47fvb24.py

 circuitpython driver lib for mcp47fvb24 dac
 using only the volatile memory on device.

 this device has 16 bit registers!!! can not use adafruit_register lib :(

 C. Hillis 4/22
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit

#register map
DAC0_R = const(0x0)
DAC1_R = const(0x1)
DAC2_R = const(0x2)
DAC3_R = const(0x3)
REF_R = const(0x8)
PD_R = const(0x9)
GS_R = const(0xa)
WL_R = const(0xb)

class MCP47FVB24:

    _DAC0 = RWBits(12, DAC0_R, 0, register_width=2, lsb_first = False)
    _DAC1 = RWBits(12, DAC1_R, 0, register_width=2, lsb_first = False)
    _DAC2 = RWBits(12, DAC2_R, 0, register_width=2, lsb_first = False)
    _DAC3 = RWBits(12, DAC3_R, 0, register_width=2, lsb_first = False)
    dac0_ref = RWBits(2, REF_R, 0, register_width=2, lsb_first = False)
    dac1_ref = RWBits(2, REF_R, 2, register_width=2, lsb_first = False)
    dac2_ref = RWBits(2, REF_R, 4, register_width=2, lsb_first = False)
    dac3_ref = RWBits(2, REF_R, 6, register_width=2, lsb_first = False)
    _POWER_DOWN = RWBits(8, PD_R, 0, register_width=2, lsb_first = False) #default 0's
    _RST = RWBit(GS_R, 7, register_width=2, lsb_first = False)
    _dac0_gain=RWBit(GS_R, 8, register_width=2, lsb_first = False)
    _dac1_gain=RWBit(GS_R, 9, register_width=2, lsb_first = False)
    _dac2_gain=RWBit(GS_R, 10, register_width=2, lsb_first = False)
    _dac3_gain=RWBit(GS_R, 11, register_width=2, lsb_first = False)

    """
    general device init. 
    lat_0 and lat_1 should be objects that change the value of the specified pin with True/False
    """
    def __init__(self, i2c_bus, addr, lat_0, lat_1):
        self.lat_0 = lat_0
        self.lat_1 = lat_1
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        self.on()

    def on(self):
        # set all outputs to 0
        self.dac0 = 0x0
        self.dac1 = 0x0
        self.dac2 = 0x0
        self.sac3 = 0x0
        self.lat_0 = False
        self.lat_1 = False
        self.lat_0 = True
        self.lat_1 = True
        #edit configs
        self.dac0_ref = 0x1
        self.dac1_ref = 0x1
        self.dac2_ref = 0x1
        self.dac3_ref = 0x1

        self.dac0_gain = True
        self.dac1_gain = True
        self.dac2_gain = True
        self.dac3_gain = True

        self._POWER_DOWN = 0x0
        #self.gain = 0xf

    def off(self):
        self._POWER_DOWN = 0xff

    """
    dac values
    please write only with 12b ints
    dac_vout = vref*val / 2^12
    """
    @property
    def dac0(self):
        return self._DAC0
    @dac0.setter
    def dac0(self, value):
        self._dac0 = value
        self.lat_0 = False
        self.lat_0 = True
    
    @property
    def dac1(self):
        return self._DAC1
    @dac1.setter
    def dac1(self, value):
        self._dac1 = value
        self.lat_1 = False
        self.lat_1 = True

    @property
    def dac2(self):
        return self._DAC2
    @dac2.setter
    def dac2(self, value):
        self._dac2 = value
        self.lat_0 = False
        self.lat_0 = True

    @property
    def dac3(self):
        return self._DAC3
    @dac3.setter
    def dac3(self, value):
        self._dac3 = value
        self.lat_1 = False
        self.lat_1 = True

    """
    dac ref's
    0x0 = vdd ref, unbuffered
    0x1 = internal band gap vref = 1.22V
    0x2 = vref pin, unbuffered
    0x3 = vref pin, buffered
    """
    """
    dac power down register
    0x0 = normal operation
    0xff = unpowered, open circuit
    """
    """
    dac gain register
    0x0 = 1x gain
    0xf = 2x gain
    """


    
    