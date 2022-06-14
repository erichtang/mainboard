"""
battery monitoring task that turns the sat to low power mode if battery low enough

working through this right now.

move this functionality to housekeeper_task...

* Author: Max Holliday
* Edited by: Caden Hillis
"""

from Tasks.template_task import Task
import time

class task(Task):
    priority = 1
    frequency = 1/10
    name = 'battery'
    color = 'orange'

    timeout = 60*60

    async def main_task(self):

        self.debug("Voltage of battery = " + str(self.cubesat.battery_voltage)  + " Threshold = " + str(self.cubesat.config['vlb']))

        # checking > vlowbatt
        if self.cubesat.battery_voltage < self.cubesat.config['vlb']:
            # setting a nvm flag that persists through power cycles
            self.cubesat.f_lowbatt=True
            # if we've timed out, don't do anything
             # this is true if we ahve previously spent a lot of time in low power mode, protects against being stuck in low powermode
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
                    self.debug('vbatt: {:.1f}V'.format(self.cubesat.battery_voltage))
                    # if the current battery voltage is greater than the allotted minimum
                    if self.cubesat.battery_voltage > self.cubesat.config['vlb']:
                        self.debug('batteries above threshold')
                        self.cubesat.f_lowbatt=False
                        break

                    # this is very very bad if we get here
                    if time.monotonic() > _timer:
                        self.debug('low batt timeout!')
                        # set timeout flag so we know to bypass
                        self.cubesat.f_lowbtout = True
                        # log (if we can)
                        try: self.cubesat.log('low batt timeout')
                        except: pass
                        break

                self.debug('waking up')
                # always wake up
                self.cubesat.powermode('normal')
                # give everything a moment to power up
                time.sleep(3)
                # restart all tasks
                for t in self.cubesat.scheduled_tasks:
                    self.cubesat.scheduled_tasks[t].start()