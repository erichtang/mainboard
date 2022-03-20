"""
`pca9543`
====================================================

CircuitPython driver for the pca9543 I2C mux

* Author(s):  C. Hillis

--------------------

"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

_cmd=bytearray(1)
_STATUS=bytearray(1)

class PCA9543:
    def __init__(self, i2c_bus, addr):
        
        print('test')
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        #if (self.read(self) != 0x00):
            #print('[ERROR][PCA9543 @ {addr}][BAD STATUS READ]')

    def read(self):
         with self.i2c_device as i2c:
             i2c.readinto(_STATUS)
         return _STATUS
    
    def clear(self):
        _cmd[0] = 0x00
        with self.i2c_device as i2c:
            i2c.write(_cmd)

    def set_ch0(self):
        _cmd[0] = 0x1
        with self.i2c_device as i2c:
            i2c.write(_cmd)
    
    def set_ch1(self):
        _cmd[0] = 0x2
        with self.i2c_device as i2c:
            i2c.write(_cmd)