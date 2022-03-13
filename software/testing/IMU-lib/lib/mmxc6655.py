# mmxc6655.py
#
# circuitpython driver lib for mmc6655 accelerometer
#
# C. Hillis 3/22

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

_cmd = bytearray(2)
_BUFFER = bytearray(8)
_cmd_read = bytearray(8)

# Register Map
INT_0 = const(0x00)
INT_1 = const(0x01)
STATUS = const(0x02)
XOUT_H = const(0x03)
XOUT_L = const(0x04)
YOUT_H = const(0x05)
YOUT_L = const(0x06)
ZOUT_H = const(0x07)
ZOUT_L = const(0x08)
TOUT = const(0x09)
INT_MASK0 = const(0x0A)
INT_MASK1 = const(0x0B)
DETECT = const(0x0C)
CONTROL = const(0x0D)
WHO_AM_I = const(0x0F)

#
WHO_AM_I_DEFAULT = const(0x05)


#

class mmxc6655(self, i2c_bus, self):

    def __init__(self, i2c_bus, self):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        self.i2c_addr = addr
        whoami = self.id_verify(self)
        if(whoami != WHO_AM_I_DEFAULT):
            print("[ERROR][IAM23080 @ ADDR: {addr}][WHO_AM_I VALUE: {whoami}]")
        #self.config
        # finish this function

    def whoami_verify(self, i2c_bus):
        _cmd[0] = WHO_AM_I
        with self.i2c_device as i2c:
            i2c.write(_cmd[0])
            i2c.readinto(_BUFFER[0])
        return(_BUFFER[0])
