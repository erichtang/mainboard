# iam20380.py
#
# circuitpython driver lib for iam20380 gyro
#
# currently is just a set-it-and-forget-it dealio for the FP/mainboard usage
#
# C. Hillis 3/22

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct

# Register Map
#SELF_TEST_X_GYRO    = const(0x00)
#SELF_TEST_Y_GYRO    = const(0x01)
#SELF_TEST_Z_GYRO    = const(0x02)
#XG_OFFS_USRH        = const(0x13)
#XG_OFFS_USRL        = const(0x14)
#YG_OFFS_USRH        = const(0x15)
#YG_OFFS_USRL        = const(0x16)
#ZG_OFFS_USRH        = const(0x17)
#ZG_OFFS_USRL        = const(0x18)
SMPLRT_DIV          = const(0x19)
CONFIG              = const(0x1A)
GYRO_CONFIG         = const(0x1B)
LP_MODE_CFG         = const(0x1E)
FIFO_EN             = const(0x23)
#FSYNC_INT           = const(0x36)
#INT_PIN_CFG         = const(0x37)
INT_ENABLE          = const(0x38)
INT_STATUS          = const(0x3A)
TEMP_OUT_H          = const(0x41)
TEMP_OUT_L          = const(0x42)
GYRO_XOUT_H         = const(0x43)
GYRO_XOUT_L         = const(0x44)
GYRO_YOUT_H         = const(0x45)
GYRO_YOUT_L         = const(0x46)
GYRO_ZOUT_H         = const(0x47)
GYRO_ZOUT_L         = const(0x48)
#SIGNAL_PATH_RESET   = const(0x68)
USER_CTRL           = const(0x6A)
PWR_MGMT_1          = const(0x6B)
PWR_MGMT_2          = const(0x6C)
#FIFO_COUNTH         = const(0x72)
#FIFO_COUNTL         = const(0x73)
#FIFO_R_W            = const(0x74)
WHO_AM_I            = const(0x75)

# Default Register Values
##PWR_MGMT_1_DEFAULT  = const(0x40)
WHO_AM_I_DEFAULT    = const(0xB5) 

class IAM20380:

    # Class Variables (NOT ALL REGISTERS AND FUNCTIONS ARE IMPLEMENTED)
    _smplrt_div = UnaryStruct(SMPLRT_DIV, "<B")
    _dlpf_cfg = RWBits(3, CONFIG, 0)
    _fs_sel = RWBits(2, GYRO_CONFIG, 3)
    _fchoice_b = RWBits(2, GYRO_CONFIG, 0)
    _gyro_cycle = RWBit(LP_MODE_CFG, 7)
    _gavg_cfg = RWBits(3, LP_MODE_CFG, 4)
    _drdy_int_en = RWBit(INT_ENABLE, 0)
    _drdy_int = RWBit(INT_STATUS, 0)
    _temp_h = UnaryStruct(TEMP_OUT_H, "<B")
    _temp_l = UnaryStruct(TEMP_OUT_L, "<B")
    _gyro_xout_h = UnaryStruct(GYRO_XOUT_H, "<B")
    _gyro_xout_l = UnaryStruct(GYRO_XOUT_L, "<B")
    _gyro_yout_h = UnaryStruct(GYRO_YOUT_H, "<B")
    _gyro_yout_l = UnaryStruct(GYRO_YOUT_L, "<B")
    _gyro_zout_h = UnaryStruct(GYRO_ZOUT_H, "<B")
    _gyro_zout_l = UnaryStruct(GYRO_ZOUT_H, "<B")
    _sig_cond_rst = RWBit(USER_CTRL, 0)
    _device_reset = RWBit(PWR_MGMT_1, 7)
    _sleep = RWBit(PWR_MGMT_1, 6)
    _clksel = RWBits(3, PWR_MGMT_1, 0)
    _who_am_i = ROBits(4, WHO_AM_I, 0)
    
    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        test = self._who_am_i
        if not test == 5: print("[ERROR][IAM20380][BAD WHO_AM_I VALUE]")
        self.ON()

    def ON(self):
        self.rst()
        self._smplrt_div = 99 # 100Hz sampling, sampling rate = 1kHz/(1+smplrt_div)
        self._dlpf_cfg = 4 #set to 20Hz LPF 1kHz sampling rate. if there is a 20Hz oscillation on this, there is a problm.
        self._fs_sel = 0 #+/- 250dps
        self._fchoice_b = 0 #dlpf NOT bypassed
        self._drdy_int_en = 1
        self._sleep = 0 #it is intiallized as 1
    
    # def low_power(self):
    #     self.rst()
    #     self.fs_sel = 0
    #     self.gyro_cycle = 1 #add what this means
    #     self.gavg_cfg = 7
    #     self.sleep = 0 

    def SLEEP(self):
        self._sleep = 1

    def rst(self):
        self._device_reset = 1
        i = self._device_reset
        while i == 1:
            i = self._device_reset #waits for reset to be completed

    def read(self):
        data_good_flag = False #is set to true if measurement goes thru
        if(self._drdy_int == True):
            x = (self._gyro_xout_h << 8) + self._gyro_xout_l
            y = (self._gyro_yout_h << 8) + self._gyro_yout_l
            z = (self._gyro_zout_h << 8) + self._gyro_zout_l
            out = [x,y,z]
            data_good_flag = True
        #raw to dps data massaging
        for meas in out:
            out[meas] = out[meas]/131 # 131LSB/dps , hardcoded in sensitivty, sorry future self
            #no idea to know what the sign of this is?
                #put 16b twos comp code here ?
                # or put null offset code here?
        if (data_good_flag == True):
            return(out)
        else:
            return(None)

    def temp(self):
        temp = (self._temp_h << 8) + (self._temp_l) # merge registers
        temp = ((temp - 25)/326.8)+25
        return(temp)

    # @property
    # def smplrt_div(self):
    #     #print("[IAM20380][SMPLRT_DIV][",hex(self._smplrt_div_data),"]")
    #     return(self._smplrt_div)
    # @smplrt_div.setter
    # def smplrt_div(self, value):
    #     self._smplrt_div = value

    # @property
    # def dlpf_cfg(self):
    #     #print("[IAM20380][CONFIG][DPLF_CFG][",bin(self._dplf_cfg),"]")
    #     return(self._dlpf_cfg)
    # @dlpf_cfg.setter
    # def dlpf_cfg(self, value):
    #     self._dlpf_cfg = value

    # @property
    # def fs_sel(self):
    #     #print("[IAM20380][GYRO_CONFIG][FS_SEL][",bin(self._fs_sel),"]")
    #     return(self._fs_sel)
    # @fs_sel.setter
    # def fs_sel(self, value):
    #     self._fs_sel = value

    # @property
    # def fchoice_b(self):
    #     #print("[IAM20380][GYRO_CONFIG][FCHOICE_B][",bin(self._fchoice_b),"]")
    #     return(self._fchoice_b)
    # @fchoice_b.setter
    # def fchoice_b(self, value):
    #     self._fchoice_b = value

    # @property
    # def gyro_cycle(self):
    #     #print("[IAM20380][LP_MODE_CFG][GYRO_CYCLE][",bin(self._gyro_cycle),"]")
    #     return(self._gyro_cycle)
    # @gyro_cycle.setter
    # def gyro_cycle(self, value):
    #     self._gyro_cycle = value

    # @property
    # def gavg_cfg(self):
    #     #print("[IAM20380][LP_MODE_CFG][GAVG_CFG][",bin(self._gavg_cfg),"]")
    #     return(self._gavg_cfg)
    # @gavg_cfg.setter
    # def gavg_cfg(self, value):
    #     self._gavg_cfg = value

    # @property
    # def temp_raw(self):
    #     temp_raw = (self._temp_h << 8) + self._temp_l
    #     #print("[IAM20380][TEMP][RAW][",temp_raw,"]")
    #     return(temp_raw)

    # @property
    # def temp(self):
    #     temp = ((self.temp_raw - 25)/326.8)+25
    #     #print("[IAM20380][TEMP][ADJ][",temp,"]")
    #     return(temp)

    # @property
    # def x_raw(self):
    #     x_raw = (self._gyro_xout_h << 8) + self._gyro_xout_l
    #     #print("[IAM20380][XOUT][R][",bin(x_raw),"]")
    #     return(x_raw)
    
    # @property
    # def y_raw(self):
    #     y_raw = (self._gyro_yout_h << 8) + self._gyro_yout_l
    #     #print("[IAM20380][YOUT][R][",bin(y_raw),"]")
    #     return(y_raw)
    
    # @property
    # def z_raw(self):
    #     z_raw = (self._gyro_zout_h << 8) + self._gyro_zout_l
    #     #print("[IAM20380][ZOUT][R][",bin(z_raw),"]")
    #     return(z_raw)
    
    # @property
    # def x(self):
    #     x = self._gyro_scale(self.x_raw)
    #     #print("[IAM20380][XOUT][",x,"][DPS]")
    #     return(x)
    
    # @property
    # def y(self):
    #     y = self._gyro_scale(self.y_raw)
    #     #print("[IAM20380][YOUT][",y,"][DPS]")
    #     return(y)
    
    # @property
    # def z(self):
    #     z = self._gyro_scale(self.z_raw)
    #     #print("[IAM20380][ZOUT][",z,"][DPS]")
    #     return(z)

    # def _gyro_scale(self, raw_input):
    #     #scale is in form LSB/dps # I AM NOT SURE IF THIS CONVERSION IS CORRECCT
    #     sw = self.fs_sel
    #     if (sw == 0): # +/- 250 dps
    #         sensitivity=131
    #         scale = 250
    #     elif (sw == 1): # +/- 500 dps
    #         sensitivity=65.5
    #         scale = 500
    #     elif (sw == 2): # +/- 1000 dps
    #         sensitivity=32.8
    #         scale = 1000
    #     else: # +/- 2000 dps
    #         sensitivity=16.4
    #         scale = 2000
    #     self._16btwos2int(raw_input)
    #     scaled_output = raw_input / scale #/ sensitivity # THIS IS W R O N G FIX LATER
    #     #print(scaled_output)
    #     return(scaled_output)
    
    # def _16btwos2int(self, value):
    #      if (value>>15==1):
    #         value = ((value ^ 0xFF)+1)*(-1)
    #         #print(value)
    #         return(value)
