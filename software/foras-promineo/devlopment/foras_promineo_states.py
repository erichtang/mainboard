"""
these functions will handle most major state transitions for the cubesat.

I  think this is superceded, so dont edit for now....
"""

import time
import usb_cdc
from debugcolor import co

"""
state dictionaries
"""
mode = {
    'startup'   : startup_dict,
    'idle'      : idle_dict,
    'safe'      : safe_dict,
    'payload'   : payload_dict
}

def startup(self, satellite):
    self.cubesat = satellite
    if usb_cdc.terminal.connected: # bypass startup
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

def idle(self, satellite):
    pass

def safe(self, satellite):
    pass

def payload(self, satellite):
    pass