# iam23080.py
#
# circuitpython driver lib for iam23080
#
# C. Hillis 3/22

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

_cmd=bytearray(2)
_BUFFER = bytearray(8)
_cmd_read = bytearray(8)

# Register Map
SELF_TEST_X_GYRO    = const(0x00)
SELF_TEST_Y_GYRO    = const(0x01)
SELF_TEST_Z_GYRO    = const(0x02)
XG_OFFS_USRH        = const(0x13)
XG_OFFS_USRL        = const(0x14)
YG_OFFS_USRH        = const(0x15)
YG_OFFS_USRL        = const(0x16)
ZG_OFFS_USRH        = const(0x17)
ZG_OFFS_USRL        = const(0x18)
SMPLRT_DIV          = const(0x19)
CONFIG              = const(0x1A)
GYRO_CONFIG         = const(0x1B)
LP_MODE_CFG         = const(0x1E)
FIFO_EN             = const(0x23)
FSYNC_INT           = const(0x36)
INT_PIN_CFG         = const(0x37)
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
SIGNAL_PATH_RESET   = const(0x68)
USER_CTRL           = const(0x6A)
PWR_MGMT_1          = const(0x6B)
PWR_MGMT_2          = const(0x6C)
FIFO_COUNTH         = const(0x72)
FIFO_COUNTL         = const(0x73)
FIFO_R_W            = const(0x74)
WHO_AM_I            = const(0x75)

# Bit Masks
#   CONFIG
FIFO_MODE           = const(0x40) #b6
EXT_SYNC_SET        = const(0x38) #b3,4,5
DPLF_CFG            = const(0x07) # b0,1,2
#   GYRO_CONFIG
XG_ST               = const(0x80) #b7
YG_ST               = const(0x40) #b6
ZG_ST               = const(0x20) #b5
FS_SEL              = const(0x18) #b3,4
FCHOICE_B           = const(0x03) #b0,1
#   LP_MODE_CFG
#   FIFO_EN
#   FSYNC_INT
#   INT_PIN_CFG
#   INT_ENABLE
#   INT_STATUS
#   SIGNAL_PATH_RESET
#   USER_CTRL
#   PWR_MGMT_1
#   PWR_MGMT_2

# Default Register Values
PWR_MGMT_1_DEFAULT  = const(0x40)
WHO_AM_I_DEFAULT    = const(0xB5)

# Initilization Defaults Set By Me
DEFAULT_DPLF_CONFIG_VALUE   = const(0x03)  #startup in 1kHz sampling w/ -3db LPF @ 41Hz
DEFAULT_SMPLRT_DIV_VALUE    = const(0xFF) #startup w/ slowest sample_rate, 3.9Hz
DEFAULT_GYRO_CYCLE_VALUE    = const(0x01) #startup in low power mode
DEFAULT_G_AVGCFG_VALUE      = const(0x00) #IDK what this really does but it is fine at 0
DEFAULT_DATA_RDY_INT_VALUE  = const(0x00)
DEFAULT_SLEEP_VALUE         = const(0x01) #default in sleep mode
DEFAULT_RST_VALUE           = const(0x00)

_cmd_read = [TEMP_OUT_H, TEMP_OUT_L, GYRO_XOUT_H, GYRO_XOUT_L, GYRO_YOUT_H, GYRO_YOUT_L, GYRO_ZOUT_H, GYRO_ZOUT_L]

class iam23080(self, i2c_bus, addr):

    def __init__(self, i2c_bus, addr):
        self.i2c_device = I2CDevice(i2c_bus, addr, probe=False)
        self.i2c_addr = addr
        whoami_check = self.whoami(self)
        if(whoami_check!=WHO_AM_I_DEFAULT):
            print("[ERROR][IAM23080 @ ADDR: {addr}][WHO_AM_I RETURNED UNEXPECTED VALUE OF {whoami_check}]")
        self.set_config(self, dplf_cfg=DEFAULT_DPLF_CONFIG_VALUE)
        self.set_gyro_config(self) #startup w/ gyro in +/- 250 DPS FS, with DLPF not bypassed
        self.set_smplrt_div(self, DEFAULT_SMPLRT_DIV_VALUE) 
        self.set_lp_mode_cfg(self,DEFAULT_GYRO_CYCLE_VALUE, DEFAULT_G_AVGCFG_VALUE)
        #self.set_fifo_en() # i dont think we will use the FIFO
        self.set_int_enable(self, DEFAULT_DATA_RDY_INT_VALUE)
        #self.set_user_control(self, )
        self.set_pwr_mgmt_1(self, DEFAULT_SLEEP_VALUE, DEFAULT_RST_VALUE)

                
    @property
    def set_config(self, fifo_mode=0x00, ext_sync_set=0x00, dplf_cfg=0x00):
        _cmd[0] = CONFIG
        _cmd[1] = 0x00
        _cmd[1] |= fifo_mode<<6
        _cmd[1] |= ext_sync_set<<3
        _cmd[1] |= dplf_cfg
        with self.i2c_device as i2c:
            i2c.write(_cmd)

    @property
    def set_gyro_config(self,xg_st=0x00, yg_st=0x00, zg_st=0x00, fs_sel=0x00, fchoice_b=0x00):
        _cmd[0] = GYRO_CONFIG
        _cmd[1] = 0x00
        _cmd[1] |= xg_st<<7
        _cmd[1] |= yg_st<<6
        _cmd[1] |= zg_st<<5
        _cmd[1] |= fs_sel<<3
        _cmd[1] |= fchoice_b<<0
        with self.i2c_device as i2c:
            i2c.write(_cmd)
    @property
    def set_smplrt_div(self, smplrt_div_value):
        _cmd[0] = SMPLRT_DIV
        _cmd[1] = 0x00
        _cmd[1] = smplrt_div_value
        with self.i2c_device as i2c:
            i2c.write(_cmd)
    
    @property
    def set_lp_mode_cfg(self, gyro_cycle, g_avgcfg):
        _cmd[0] = LP_MODE_CFG
        _cmd[1] = 0x00
        _cmd[1] |= gyro_cycle<<7
        _cmd[1] |= g_avgcfg<<4
        with self.i2c_device as i2c:
            i2c.write(_cmd)

#    @property
#    set_fifo_enable()        

    @property
    def set_int_enable(self, data_rdy_int_en):
        _cmd[0] = INT_ENABLE
        _cmd[1] = 0x00
        _cmd[1] |= data_rdy_int_en
        with self.i2c_device as i2c:
            i2c.write(_cmd)

#    @property
#    def set_user_control(self, fifo_en_value=0x00, fifo_rst_value=0x00, sig_cond_rst=0x00):
#        _cmd[0] = USER_CTRL
#        _cmd[1] = 0x00
#        _cmd[1] |= fifo_en_value

    @property
    def set_pwr_mgmt_1(self, sleep_value, rst_value):
        _cmd[0] = PWR_MGMT_1
        _cmd[1] = 0x00
        _cmd[1] |= sleep_value<<6
        _cmd[1] |= rst_value<<7
        with self.i2c_device as i2c:
            i2c.write(_cmd)

    @property
    def sleep(self, sleep):
        _cmd[0] = PWR_MGMT_1
        with self.i2c_device as i2c:
            _cmd[1] = i2c.read(PWR_MGMT_1)
        _cmd[1] &= (~0x01<<6) #clear
        _cmd[1] |= sleep<<6 #set

    @property
    def read(self):
        with self.i2c_device as i2c:
            for byte in _cmd_read:
                i2c.write(_cmd_read[byte])
                i2c.read(_BUFFER[byte])
        _temp_out = ((_BUFFER[0] << 8) | _BUFFER[1])
        #_temperature # temp to 2 bits of decimal precision
        _temp_out = tmp_adj(_temp_out)
        _xg_out = ((_BUFFER[2] << 8) | _BUFFER[3])
        _yg_out = ((_BUFFER[4] << 8) | _BUFFER[5])
        _zg_out = ((_BUFFER[6] << 8) | _BUFFER[7])
        return(_temp_out, _xg_out, _yg_out, _zg_out)

    def tmp_adj(temp): # implemnt temp in deg c with 2 bits of decimal precidsion
        return temp

    def whoami(self):
        _cmd[0] = WHO_AM_I
        
        with self.i2c_device as i2c:
            i2c.write(_cmd[0])
            iwhoami = i2c.read(_BUFFER[0])
        return(whoami)