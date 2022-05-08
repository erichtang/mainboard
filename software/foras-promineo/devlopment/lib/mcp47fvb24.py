"""
 mcp47fvb24.py

 circuitpython driver lib for mcp47fvb24 dac
 using only the volatile memory on device.

 this device has 16 bit registers!!!

 C. Hillis 4/22
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

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

    _DAC0 = RWBits(12, DAC0_R, 0)
    _DAC1 = RWBits(12, DAC1_R, 0)
    _DAC2 = RWBits(12, DAC2_R, 0)
    _DAC3 = RWBits(12, DAC3_R, 0)
    _DAC0_REF = RWBits(2, REF_R, 0)
    _DAC1_REF = RWBits(2, REF_R, 2)
    _DAC2_REF = RWBits(2, REF_R, 4)
    _DAC3_REF = RWBits(2, REF_R, 6)
    _POWER_DOWN = RWBits(8, PD_R, 0) #default 0's
    _RST = RWBit(GS_R, 7)
    _GAIN = RWBits(4, GS_R, 8)

    """
    general device init. 
    lat_0 and lat_1 should be objects that change the value of the specified pin with True/False
    """
    def __init__(self, i2c_bus, addr, lat_0, lat_1):
        self.lat_0 = lat_0
        self.lat_1 = lat_1
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        self.on(self)

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
        self.dac0_ref = 0x3
        self.dac1_ref = 0x3
        self.dac2_ref = 0x3
        self.dac3_ref = 0x3
        self.power_down = 0x0
        self.gain = 0xf

    def off(self):
        self.power_down = 0xff

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
    @property
    def dac0_ref(self):
        return self._DAC0_REF
    @dac0_ref.setter
    def dac0_ref(self, value):
        self._DAC0_REF = value

    @property
    def dac1_ref(self):
        return self._DAC1_REF
    @dac1_ref.setter
    def dac1_ref(self, value):
        self._DAC1_REF = value

    @property
    def dac2_ref(self):
        return self._DAC2_REF
    @dac2_ref.setter
    def dac2_ref(self, value):
        self._DAC2_REF = value

    @property
    def dac3_ref(self):
        return self._DAC3_REF
    @dac3_ref.setter
    def dac3_ref(self, value):
        self._DAC3_REF = value

    """
    dac power down register
    0x0 = normal operation
    0xff = unpowered, open circuit
    """
    @property
    def power_down(self):
        return self._POWER_DOWN
    @power_down.setter
    def power_down(self, value):
        self._POWER_DOWN = value


    """
    dac power down register
    0x0 = 1x gain
    0xf = 2x gain
    """
    @property
    def gain(self):
        return self._GAIN
    @gain.setter
    def gain(self, value):
        self._GAIN = value


    
    