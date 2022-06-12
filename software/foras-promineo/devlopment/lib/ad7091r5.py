"""
 ad7091R5.py

 circuitpython driver lib for ad7091 adc

 this devices registers are 16b!

* Author: Caden Hillis
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit

CONV = const(0x0)
CH = const(0x1)
CONFIG = const(0x2)
ALERT = const(0x3)

class AD7091R5:


    _conv_rslt = ROBits(15, CONV, 0, register_width=2, lsb_first = False)
    ch0_en = RWBit(CH, 0)
    ch1_en = RWBit(CH, 1)
    ch2_en = RWBit(CH, 2)
    ch3_en = RWBit(CH, 3)
    _ref = RWBit(CONFIG, 0, register_width=2, lsb_first = False)
    _p_down = RWBit(CONFIG, 1, register_width=2, lsb_first = False)
    _gp01 = RWBit(CONFIG, 2, register_width=2, lsb_first = False)
    _cycle = RWBits(2, CONFIG, 6, register_width=2, lsb_first = False)
    _auto = RWBit(CONFIG, 8, register_width=2, lsb_first = False)
    _srst = RWBit(CONFIG, 9, register_width=2, lsb_first = False)
    _cmd = RWBit(CONFIG, 10, register_width=2, lsb_first = False)
    _alrt_drv_type = RWBit(CONFIG, 15, register_width=2, lsb_first = False)
    _alrt_en= RWBit(CONFIG, 4, register_width=2, lsb_first = False)
    busy= RWBit(CONFIG, 5, register_width=2, lsb_first = False)
    _alert = ROBits(8, ALERT, 0)
  
    """
    general init routine
    """
    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        #if not self.config_0 == 0xf: print("[ERROR][PIB][DAC][BAD CONFIG VAL]", self.config_0)
        self.on()

    def on(self):
        self.ch0_en = True
        self._power_down = False
        self._ref = True
        self._cycle = 0x3 #1.25ksps
        self._auto = False
        self._cmd = True
        self._alrt_drv_type = True
        self._alrt_en = True

    def off(self):
        self._power_down = True
        
    @property
    def read(self):
        temp = self._conv_rslt
        reading = {
            'rd' : temp & 0xfff, #12 bits
            'ch' : (temp & 0xf000) >> 13, # bits 13, 14
        }
        return reading
