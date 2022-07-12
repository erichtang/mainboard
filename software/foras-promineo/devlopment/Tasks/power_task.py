"""
TODO: not implemented. need to move battery_task.py code here and do additional handling for bad circumstances that the cubesat should react to.
polling various values to direct satellite operating modes. monitors batteries, temps, and current.
    has elements of battery-task BUT has various thresholds for payload operation.

* Author: Caden Hillis
"""

from Tasks.template_task import Task
import time

class task(Task):
    name = 'power'
    color = 'orange'

    d_cfg = {
        'priority' : 2,
        'frequency' : 1/60,
        'timeout' : 60*60,
        'vhb'   : 8.15
    }

    async def main_task(self):

        #get power telemetry
        power_telemetry = {
            'battery_voltage'       : self.cubesat.battery_voltage,
            'solar_voltage'         : self.cubesat.solar_voltage,
            'payload_voltage'       : self.cubesat.payload_voltage,
            'rf_voltage'            : self.cubesat.rf_voltage,
            'bus_current'           : self.cubesat.bus_current,
            'charge_current'        : self.cubesat.charge_current,
            'charging'              : self.cubesat.solar_charging,
            'timestamp'             : (time.time()-self.cubesat.BOOTTIME)
        }

        """
        This new section for soft limits on overcharge needs to be debugged when the FW is updated.
        """
        # TODO check for soft limits on battery ovp
        # if we are charging and nearing 80% charge TODO calc voltage this is at
        if power_telemetry['charging'] & (power_telemetry['battery_voltage'] > self.cfg['vhb']):
            # turn off charger
            # not in FW yet
            pass
        #if we are not charging and below 80% charge
        elif (not power_telemetry['charging']) & (power_telemetry['battery_voltage'] > self.cfg['vhb']):
            # turn on charger
            # not in FW yet
            pass

        if 'power' in self.cubesat.data_cache:
            # log if charging started/stopped
            if power_telemetry['charging'] != self.cubesat.data_cache['power']['charging']:
                self.debug('charging = {}'.format(power_telemetry['charging']), log=True)
        
        # update data cache
        self.cubesat.data_cache.update({'power':power_telemetry})

        # debug print
        self.debug("Power Telemetry: ")
        for key in power_telemetry:
            self.debug('{} : {}'.format(str(key), str(power_telemetry[key])), 2)

        """
        checking > vlowbatt
        if < vlowbat this task will enter a low-battery timeout state where:
            it will stop all other tasks.
            sleep, check voltage
            if timeout amount of time has been exceeded, the device enters a "low battery timeout" where it exits the mode and returns to normal operations.
                if it times out, it will also do an emergency beacon.
        """
        if power_telemetry['battery_voltage'] < self.cubesat.config['vlb']:
            # setting a nvm flag that persists through power cycles
            self.cubesat.f_lowbatt=True
            # if we've timed out, don't do anything
             # this is true if we have previously spent a lot of time in low power mode, protects against being stuck in low powermode
            if self.cubesat.f_lowbtout:
                self.debug('lowbatt timeout flag set! skipping...')
            else:
                # setting the time to stay asleep
                _timer=time.monotonic()+self.timeout
                self.debug('low battery detected!', 2)
                # stop all tasks
                for t in self.cubesat.scheduled_tasks:
                    self.cubesat.scheduled_tasks[t].stop()
                # setting powermode of the satellite to a minimum
                self.cubesat.powermode('minimum')

                # while the maximum time has not been exceeded
                while time.monotonic() < _timer:
                    # sleep for a 10th our remaining time
                    _sleeptime = self.timeout/10 
                    self.debug('sleeping for {}s'.format(_sleeptime))
                    time.sleep(_sleeptime)

                    # get new voltage 
                    battery_voltage = self.cubesat.battery_voltage

                    self.debug('vbatt: {:.1f}V'.format(battery_voltage))
                    # if the current battery voltage is greater than the allotted minimum
                    if battery_voltage > self.cubesat.config['vlb']:
                        self.debug('batteries above threshold')
                        self.cubesat.f_lowbatt=False
                        break

                    # this is very very bad if we get here
                    if time.monotonic() > _timer:
                        self.debug('low batt timeout!')
                        # set timeout flag so we know to bypass
                        self.cubesat.f_lowbtout = True
                        # log (if we can)
                        try: self.debug('low batt timeout', log=True)
                        except: pass
                        break

                try: self.debug('waking up', log=True)
                except: pass

                # always wake up
                self.cubesat.powermode('normal')
                # give everything a moment to power up
                time.sleep(3)

                # TODO  add an emergency beacon here

                # restart all tasks 
                for t in self.cubesat.scheduled_tasks:
                    self.cubesat.scheduled_tasks[t].start()