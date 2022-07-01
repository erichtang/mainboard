"""
TODO -- foras promineo state definiton, transition, and execution is still being devloped. I have no doubt this could change.
startup task for foras promineo. 
    Refer to the state transition table for mission operating states.

at startup, stops all non-critical tasks and preforms an initial startup / checkout procedure.
at the end, it will release the satellite to idle mode, by starting all the tasks that were stopped initally.

this task is not-blocking, it will change settings for other task execution i.e. ADCS detumble / calibration
    also, it will permimately not do inital startup actions if the NVM flag is set. (i.e. burn wires...)

can go into safe mode from here.

* Author: Caden Hillis
"""
import usb_cdc # TODO remove reference to usb_cdc, as simulation mode is now implemented differently than imagined here... Implement startup simulation task TOO!!
from Tasks.template_task import Task

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
            'done'      : False
            }

    async def main_task(self):
        if not self.cubesat.f_deployed: #f_deployed is set AFTER FLIGHT startup has been completed. there is NO changing it back except manually.
            #preform deployment operaton
            self.startup() # sets settings and other things for startup mode
        else:
            # set default idle settings
            self.cubesat.scheduled_tasks['startup'].stop()

    def startup(self):
        if usb_cdc.terminal.connected:
            self.debug('[STARTUP BYPASSED][REASON: USB TERMINAL]')
            self.cubesat.scheduled_tasks['startup_task'].stop()
            return
        if not self.startup_steps['init']:
            #do things here
            # unscheduled all non-critical tasks and begin initial startup
            pass
        elif not self.startup_steps['deploy']:
            #do next step of cubesat initial startup
            pass
        #TODO implement and define all startup steps
