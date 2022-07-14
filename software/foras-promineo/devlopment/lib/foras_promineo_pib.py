"""
foras_promineo_pib.py
====================================================================
Foras Promineo mission-specific payload interface board library
    this board also has the mt drivers, irridium, and other things
only pertains to the pib, see foras_promineo_payload.py for things on the payload.

* Authors C. Hillis
====================================================================

"""

import imu
import max7311
import mcp47fvb24
import ad7091r5
import rockblock_9603

class PIB():

    def __init__(self, satellite):
        """
        inherits satellite from pycubed.py
        init's FP pib devices and any functionality for managing them.
        """
        self.cubesat = satellite

        self.hardware = {
            'IMU'       : False,
            'IO_EXP'    : False,
            'DAC'       : False,
            'ADC'       : False,
            'ROCKBLOCK'  : False,
            #other pib devices here
        }

        # define digital IO

        
        # Initialize IMU
        try:
            self.imu = imu.IMU(self.cubesat, 'PIB][IMU', mux_addr=0x71)
            self.hardware['IMU'] = True
            self.cubesat.log('[INIT][PIB][IMU]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][IMU]: {}'.format(e))

        #define IO_EXP
        try:
            self.io_exp = max7311.MAX7311(self.cubesat.i2c1, 0x20)
            #io exp signal names and default states
            self.n_dac_lat0 = self.io_exp.out_00 
            self.n_dac_lat0 = True
            self.n_dac_lat1 = self.io_exp.out_01
            self.n_dac_lat1 = True
            self.n_amp_shdn_xy = self.io_exp.out_02
            self.n_amp_shdn_xy = False
            self.n_amp_shdn_z = self.io_exp.out_03
            self.n_amp_shdn_z = False
            self.drv_ph_x = self.io_exp.out_04
            self.drv_ph_x = False
            self.drv_en_x = self.io_exp.out_05
            self.drv_en_x = False
            self.n_drv_slp_x = self.io_exp.out_06
            self.n_drv_slp_x = False
            self.drv_ph_y = self.io_exp.out_07
            self.drv_ph_y = False
            self.drv_en_y = self.io_exp.out_08
            self.drv_en_y = False
            self.n_drv_slp_y = self.io_exp.out_09
            self.n_drv_slp_y = False
            self.drv_ph_z = self.io_exp.out_10
            self.drv_ph_z = False
            self.drv_en_z = self.io_exp.out_11
            self.drv_en_z = False
            self.n_drv_slp_z = self.io_exp.out_12
            self.n_drv_slp_z = False
            #self.io_exp.out_13 = self.adc_alert_busy # input # not implemented in max3711 lib
            self.n_dac_rst = self.io_exp.out_14
            self.n_dac_rst = True
            self.hardware['IO_EXP'] = True
            self.cubesat.log('[INIT][PIB][IO EXP]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][IO EXP]: {}'.format(e))
        
        #define DAC
        try:
            self.dac = mcp47fvb24.MCP47FVB24(self.cubesat.i2c1, 0x60, self.n_dac_lat0, self.n_dac_lat1)
            self.hardware['DAC'] = True
            self.cubesat.log('[INIT][PIB][DAC]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][DAC]: {}'.format(e))

        #define ADC
        try:
            self.adc = ad7091r5.AD7091R5(self.cubesat.i2c1, 0x2F)
            self.hardware['ADC'] = True
            self.cubesat.log('[INIT][PIB][ADC]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][ADC]: {}'.format(e))
        
        #define rockblock
        """
        try:
            self.rockblock = rockblock_9602.rockblock_9602(self)
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][ROCKBLOCK]' + str(e))
        """

    def powermode(self, mode):
        if 'min' in mode:
            if self.hardware['IMU']:
                self.imu.powermode('min')
            if self.hardware['IO_EXP']:
                # add line clear io exp?
                self.io_exp.off()
            if self.hardware['DAC']:
                self.dac.off()
            if self.hardware['ADC']:
                self.adc.off()
        elif 'norm' in mode:
            if self.hardware['IMU']:
                self.imu.powermode('norm')
            if self.hardware['IO_EXP']:
                 # add line to restore default ioexp values?
                self.io_exp.on()
            if self.hardware['DAC']:
                self.dac.on()
            if self.hardware['ADC']:
                self.adc.on()
    """
    temporarty mt drive function. final implementation of this would actuate based upone a given moment, direction, and axis.
    this can probably be written better in the future
    """
    def drive_magnetotorquer(self, axis, direction, current, duration):
        x_axis_d = {
            'dac' : self.dac.dac0, 
            'amp_shdn' : self.n_amp_shdn_xy,
            'drv_ph' : self.drv_ph_x,
            'drv_en' : self.drv_en_x,
            'drv_slp' : self.n_drv_slp_x,
            'adc_ch' : self.adc.ch0_en
        }
        y_axis_d = {
            'dac' : self.dac.dac1, 
            'amp_shdn' : self.n_amp_shdn_xy,
            'drv_ph' : self.drv_ph_y,
            'drv_en' : self.drv_en_y,
            'drv_slp' : self.n_drv_slp_y,
            'adc_ch' : self.adc.ch1_en
        }
        z_axis_d = {
            'dac' : self.dac.dac2, 
            'amp_shdn' : self.n_amp_shdn_z,
            'drv_ph' : self.drv_ph_z,
            'drv_en' : self.drv_en_z,
            'drv_slp' : self.n_drv_slp_z,
            'adc_ch' : self.adc.ch2_en
        }
        axis_d = {
            'x' : x_axis_d,
            'y' : y_axis_d,
            'z' : z_axis_d,
        }
        # set dac
        # turn on amp
        # set h-bridge
        # turn on h-bridge
        # read sense
        # turn off h-bridge