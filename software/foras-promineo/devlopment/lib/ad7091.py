"""
 ad7091.py

 circuitpython driver lib for ad7091 dac

 this devices registers are 16b!

 C. Hillis 4/22
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

CONV = const(0x0)
CH = const(0x1)
CONFIG = const(0x2)

class AD7091:

    _CONV_RSLT = ROBits(12, CONV, 0)
    _CONV_CH = RWBits(2, CONV, 13)
    _CH0_EN = RWBit(CH, 0)
    _CH1_EN = RWBit(CH, 1)
    _CH2_EN = RWBit(CH, 2)
    _CH3_EN = RWBit(CH, 3)
    _P_DOWN = RWBits(2, CONFIG, 0)
    _BUSY = RWBit(CONFIG, 5)
    _CYCLE = RWBits(2, CONFIG, 6)
    _AUTO = RWBit(CONFIG, 7)
    _SRST = RWBit(CONFIG, 8)
    _CMD = RWBit(CONFIG, 9)

  
    """
    general init routine
    """
    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        if not self.config_0 == 0xf: print("[ERROR][PIB][DAC][BAD CONFIG VAL]", self.config_0)
        self.on(self)

    #when turned on, channel just needs to be set -- then turned off unless code to handle ch in the reading dict exists
    def on(self):
        self.ch0_en = False
        self.ch1_en = False
        self.ch2_en = False
        self.ch3_en = False
        self.power_down = 0x1
        self.cycle = 0x3 #1.25ksps
        self.auto = True
        self.cmd = False
        pass

    def off(self):
        self.ch0_en = False
        self.ch1_en = False
        self.ch2_en = False
        self.ch3_en = False
        self.power_down = 0x3
        pass

    @property
    def read(self):
        reading = {
            'rd' : self._CONV_RSLT,
            'ch' : self._CONV_CH,
        }
        return reading

    @property
    def ch0_en(self):
        return self._CH0_EN
    @ch0_en.setter
    def ch0_en(self, value):
        self._CH0_EN = value

    @property
    def ch1_en(self):
        return self._CH1_EN
    @ch1_en.setter
    def ch1_en(self, value):
        self._CH1_EN = value

    @property
    def ch2_en(self):
        return self._CH2_EN
    @ch2_en.setter
    def ch2_en(self, value):
        self._CH2_EN = value
    
    @property
    def ch3_en(self):
        return self._CH3_EN
    @ch3_en.setter
    def ch3_en(self, value):
        self._CH3_EN = value

    @property
    def power_down(self):
        return self._P_DOWN
    @power_down.setter
    def power_down(self, value):
        self._P_DOWN = value

    @property
    def busy(self):
        return self._BUSY

    @property
    def cycle(self):
        return self._CYCLE
    @cycle.setter
    def cycle(self, value):
        self.cycle = value

    @property
    def auto(self):
        return self._AUTO
    @auto.setter
    def auto(self, value):
        self._AUTO = value

    @property
    def s_rst(self):
        return self._SRST
    @s_rst.setter
    def s_rst(self, value):
        self._SRSTr = value

    @property
    def cmd(self):
        return self._CMD
    @cmd.setter
    def cmd(self, value):
        self._CMD = value
    

    