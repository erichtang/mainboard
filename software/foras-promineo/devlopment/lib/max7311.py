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
    out_00 = RWBit(OUT_0, 0)
    out_01 = RWBit(OUT_0, 1)
    out_02 = RWBit(OUT_0, 2)
    out_03 = RWBit(OUT_0, 3)
    out_04 = RWBit(OUT_0, 4)
    out_05 = RWBit(OUT_0, 5)
    out_06 = RWBit(OUT_0, 6)
    out_07 = RWBit(OUT_0, 7)
    out_08 = RWBit(OUT_1, 0)
    out_09 = RWBit(OUT_1, 1)
    out_10 = RWBit(OUT_1, 2)
    out_11 = RWBit(OUT_1, 3)
    out_12 = RWBit(OUT_1, 4)
    out_13 = RWBit(OUT_1, 5)
    out_14 = RWBit(OUT_1, 6)
    out_15 = RWBit(OUT_1, 7)
    config_0 = UnaryStruct(CONFIG_1, '<B')
    config_1 = UnaryStruct(CONFIG_2, '<B')
    
    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        #if not self.config_0 == 0xf: print("[ERROR][PIB][MAX7311][BAD CONFIG VAL]" + self.config_0)
        #self.on(self)

    def on(self):
        self.config_0 = 0x0
        self.config_1 = 0x0

    def off(self):
        self.config_0 = 0xf
        self.config_1 = 0xf