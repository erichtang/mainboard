"""
TODO: not tested
polling temps
    has elements of battery-task BUT has various thresholds for payload operation.

* Author: Caden Hillis
"""

from Tasks.template_task import Task
import time

class task(Task):
    name = 'temp'
    color = 'orange'

    d_cfg = {
        'priority' : 2,
        'frequency' : 1/30,
        'otp' : 50 # over temp threshold, turns off devices if at this temperature
    }

    async def main_task(self):

       # check temps
       # TODO updaqte this with next rev of MB and FW
        temp_telemetry = {
            'mcu_temp'              : 0,
            'imu_temp'              : 0,
            'batt_temp'             : 0,
            'solar_charger_temp'    : 0,
            'payload_reg_temp'      : 0,
            'rf_reg_temp'           : 0,
            'ntc1_temp'             : 0,
            'ntc1_temp'             : 0,
            'ntc1_temp'             : 0,
            'ntc4_temp'             : 0,
            'solar_tle_1_temp'      : 0,
            'solar_tle_2_temp'      : 0,
            'solar_tle_3_temp'      : 0,
            'solar_tle_4_temp'      : 0,
            'star_tracker_temp'     : 0,
            'pib_imu_temp'          : 0,
            'payload_openmv_temp'   : 0,
        }

        # update data cache
        self.cubesat.data_cache.update({'temp':temp_telemetry})

        # print
        self.debug("Temperature Telemetry: ")
        for key in temp_telemetry:
            self.debug('{} : {}'.format(str(key), str(temp_telemetry[key])),2)

        # check for otp's
        for key in temp_telemetry:
            # send it to the handler function if it is out of bounds
            if temp_telemetry[key] >= self.cfg['otp']:
                self.temporary_otp_handler(key, temp_telemetry[key])

    def temporary_otp_handler(self, key, temp):
        self.log_otp(key, temp)
        pass

    def log_otp(self, key, temp):
        self.debug('OTP WARNING: {} : {} degC'.format(str(key), str(temp)))
