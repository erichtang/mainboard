"""
state handler for foras promineo.
sets task settings according to state device state. 

in progress
"""
from Tasks.template_task import Task
import time
import usb_cdc
import state_settings

class task(Task):
    priority = 1
    frequency = 1
    name = 'startup'
    color = 'red'
   
    def __init__(self, satellite): 

        self.cubesat = satellite 

        # some example startup steps that need to happen before startup releases to idle mode
        # code in handoff from startup to low power though
        self.startup_steps = {
            'init'  : False,
            'deploy' : False,
            'detumble' : False,
            'calibrate' : False,
            }

    async def main_task(self):
        
        if not self.cubesat.f_deployed: #f_deployed should only be set AFTER FLIGHT startup has been completed. there is NO changing it back except manually.
            #preform deployment operaton
            self.startup() # sets settings and other things for startup mode
        else:
            # set default idle settings
            self.cubesat.scheduled_tasks['startup_task'].stop()

    def startup(self):
        if usb_cdc.terminal.connected:
            self.debug('[STARTUP BYPASSED][REASON: USB TERMINAL]')
            self.cubesat.scheduled_tasks['startup_task'].stop()
            return
        elif not self.startup_steps['init']:
            #do things here
            # unscheduled all non-critical tasks and begin initial startup
            pass
        elif not self.startup_steps['deploy']:
            #do next step of cubesat initial startup
            pass

        #todo implement and define all startup steps
