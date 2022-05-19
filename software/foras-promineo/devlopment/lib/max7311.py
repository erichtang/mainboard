"""
 max7311.py

 circuitpython driver lib for max7311 io-exp

 only init'ing funcs we need

 C. Hillis 4/22
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

#Register Map
OUT_0     = const(0x2)
OUT_1     = const(0x3)
CONFIG_1 = const(0x6)
CONFIG_2 = const(0x7)


class MAX7311:

    #class variables
    _OUT_00 = RWBit(OUT_0, 0)
    _OUT_01 = RWBit(OUT_0, 1)
    _OUT_02 = RWBit(OUT_0, 2)
    _OUT_03 = RWBit(OUT_0, 3)
    _OUT_04 = RWBit(OUT_0, 4)
    _OUT_05 = RWBit(OUT_0, 5)
    _OUT_06 = RWBit(OUT_0, 6)
    _OUT_07 = RWBit(OUT_0, 7)
    _OUT_08 = RWBit(OUT_1, 0)
    _OUT_09 = RWBit(OUT_1, 1)
    _OUT_10 = RWBit(OUT_1, 2)
    _OUT_11 = RWBit(OUT_1, 3)
    _OUT_12 = RWBit(OUT_1, 4)
    _OUT_13 = RWBit(OUT_1, 5)
    _OUT_14 = RWBit(OUT_1, 6)
    _OUT_15 = RWBit(OUT_1, 7)
    _config_0 = UnaryStruct(CONFIG_1, '<B')
    _config_1 = UnaryStruct(CONFIG_2, '<B')

    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        if not self.config_0 == 0xf: print("[ERROR][PIB][MAX7311][BAD CONFIG VAL]", self.config_0)
        self.on(self)

    def on(self):
        self.config_0 = 0x0
        self.config_1 = 0x0

    def off(self):
        self.config_0 = 0xf
        self.config_1 = 0xf

    # Config setting --------------------------
    @property
    def config_0(self):
        return self._config_0
    @config_0.setter
    def config_0(self, value):
        self._config_0 = value
    
    @property
    def config_1(self):
        return self._config_1
    @config_1.setter
    def config_1(self, value):
        self._config_1 = value

    # Output setting --------------------------
    @property
    def out_0(self):
        return self._OUT_00
    @out_0.setter
    def out_0(self, value):
        self._OUT_00 = value
        
    @property
    def out_1(self):
        return self._OUT_01
    @out_1.setter
    def out_1(self, value):
        self._OUT_01 = value
    
    @property
    def out_2(self):
        return self._OUT_02
    @out_2.setter
    def out_2(self, value):
        self._OUT_02 = value
    
    @property
    def out_3(self):
        return self._OUT_03
    @out_3.setter
    def out_3(self, value):
        self._OUT_03 = value

    @property
    def out_4(self):
        return self._OUT_04
    @out_4.setter
    def out_4(self, value):
        self._OUT_04 = value

    @property
    def out_5(self):
        return self._OUT_05
    @out_5.setter
    def out_5(self, value):
        self._OUT_05 = value

    @property
    def out_6(self):
        return self._OUT_06
    @out_6.setter
    def out_6(self, value):
        self._OUT_06 = value
    
    @property
    def out_7(self):
        return self._OUT_07
    @out_7.setter
    def out_7(self, value):
        self._OUT_07 = value
    
    @property
    def out_8(self):
        return self._OUT_08
    @out_8.setter
    def out_8(self, value):
        self._OUT_08 = value

    @property
    def out_9(self):
        return self._OUT_09
    @out_9.setter
    def out_9(self, value):
        self._OUT_09 = value

    @property
    def out_10(self):
        return self._OUT_10
    @out_10.setter
    def out_10(self, value):
        self._OUT_10 = value

    @property
    def out_11(self):
        return self._OUT_11
    @out_11.setter
    def out_11(self, value):
        self._OUT_11 = value

    @property
    def out_12(self):
        return self._OUT_12
    @out_12.setter
    def out_12(self, value):
        self._OUT_12 = value

    @property
    def out_13(self):
        return self._OUT_13
    @out_13.setter
    def out_13(self, value):
        self._OUT_13 = value

    @property
    def out_14(self):
        return self._OUT_14
    @out_14.setter
    def out_14(self, value):
        self.out_14 = value

    @property
    def out_15(self):
        return self._OUT_15
    @out_15.setter
    def out_15(self, value):
        self._OUT_15 = value