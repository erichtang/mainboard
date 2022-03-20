# mmc5983.py
#
# circuitpython driver lib for mmc5983 magnetometer
#
# C. Hillis 3/22

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

_cmd = bytearray(2)
_BUFFER = bytearray(8)
_cmd_read = bytearray(8)

# Register Map
XOUT0               = const(0x00) #Xout [17:10]
XOUT1               = const(0x01) #Xout [9:2]
YOUT0               = const(0x02)
YOUT1               = const(0x03)
ZOUT0               = const(0x04)
ZOUT1               = const(0x05)
XYZOUT              = const(0x06) #Xout[1:0], Yout[1:0], Zout[1:0]∫\
TOUT                = const(0x07)
STATUS              = const(0x08)
INTERNAL_CONTROL_0  = const(0x09)
INTERNAL_CONTROL_1  = const(0x09)
INTERNAL_CONTROL_2  = const(0x09)
INTERNAL_CONTROL_3  = const(0x09)
PRODUCT_ID_1        = const(0x0A)

# Default Register Values
PRODUCT_ID_1_VALUE  = const(0x03) # the rest of the registers are 0x00 initally

# Initilization Default Setting
CM_FREQ_VALUE       = const (0x05) # init default of 100Hz zampling if 
CMM_EN_VALUE        = const (0x01) # cmm en value is 1

_cmd_read = [XOUT0, XOUT1, YOUT0, YOUT1, ZOUT0, ZOUT1, XYZOUT, TOUT]

class MMC5983:

    #move register def's to private variables with the ROBits and UnaryStruct classes

    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        #self.config(self, CM_FREQ_VALUE, CMM_EN_VALUE)

    # @property
    # def read_status(self):
    #     _cmd[0] = STATUS
    #     with self.i2c_device as i2c:
    #         i2c.write(_cmd[0])
    #         i2c.readinto(_BUFFER[0])
    #     return(_BUFFER[0])

    # @property
    # def config(self, cm_freq, cmm_en):
    #     #IC0
    #         #not implemented
    #     #IC1
    #         #not implemented
    #     #IC2
    #     _cmd[0] = INTERNAL_CONTROL_2
    #     _cmd[1] = 0x00
    #     _cmd[1] |= cm_freq | (cmm_en<<3)
    #     with self.i2c_device as i2c:
    #         i2c.write(_cmd)
    #     #IC3
    #         #not implemented
    #         #look into using the external field for testing the sensor function
        
    # @property
    # def read(self):
    #     for byte in _cmd_read:
    #         with self.i2c_device as i2c:
    #             i2c.write(_cmd[byte])
    #             i2c.readinto(_BUFFER[byte])
    #     xm_out = _BUFFER[0]<<10 | _BUFFER[1]<<2 | (((_BUFFER[6]) & 0x30)>>4)
    #     ym_out = _BUFFER[2]<<10 | _BUFFER[3]<<2 | (((_BUFFER[6]) & 0x0C)>>2)
    #     zm_out = _BUFFER[4]<<10 | _BUFFER[5]<<2 | ((_BUFFER[6]) & 0x03)
    #     tmp_out = (_BUFFER[7] * 0.8) - 75 # in degc, maybe do a q so it doesnt use floating point?
    #     return(xm_out, ym_out, zm_out, tmp_out)

    # @property
    # def read_status(self):
    #     _cmd[0] = STATUS
    #     with self.i2c_devicen as i2c:
    #         i2c.write(_cmd[0])
    #         i2c.readinto(_BUFFER[0])
    #         return(_BUFFER[0])
