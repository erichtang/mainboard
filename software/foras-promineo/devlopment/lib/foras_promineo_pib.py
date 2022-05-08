"""
foras_promineo_pib.py
====================================================================
Foras Promineo mission-specific payload interface board library
    this board also has the mt drivers, irridium, and other things
only pertains to the pib, see foras_promineo_payload.py for things on the payload.

* Authors C. Hillis
4/6
====================================================================

"""

import sli_imu
import max7311
import mcp47fvb24
import ad7091
import rockblock_9602

class PIB():

    def __init__(self, satellite):
        """
        inherits superclass satellite from pycubed.py
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
            self.imu = sli_imu.IMU(self.cubesat, mux_addr=0x7A)
            self.hardware['IMU'] = True
            self.cubesat.log('[INIT][PIB][IMU]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][IMU]' + str(e))

        #define IO_EXP
        try:
            self.io_exp = max7311.MAX7311(self.cubesat.i2c1, 0x90)
            self.hardware['IO_EXP'] = True
            self.cubesat.log('[INIT][PIB][IO EXP]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][IO EXP]' + str(e))

        #define DAC
        try:
            self.dac = mcp47fvb24.MCP47FVB24(self.cubesat.i2c1, 0x60, self.io_exp.out_0, self.io_exp.out_1)
            self.hardware['DAC'] = True
            self.cubesat.log('[INIT][PIB][DAC]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][DAC]' + str(e))

        #define ADC
        try:
            self.adc = ad7091.AD7091(self.cubesat.i2c1, 0x2F)
            self.hardware['ADC'] = True
            self.cubesat.log('[INIT][PIB][ADC]')
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][ADC]' + str(e))

        #define irridium
        """
        try:
            self.rockblock = rockblock_9602.rockblock_9602(self)
        except Exception as e:
            self.cubesat.log('[ERROR][PIB][ROCKBLOCK]' + str(e))
        """


    def reinit(self): ## call this in satellite.reinit
        pass

    def powermode(self, mode): ## call this in satellite.reinit
        pass
