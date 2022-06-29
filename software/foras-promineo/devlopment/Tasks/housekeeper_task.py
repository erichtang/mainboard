"""
TODO: not implemented. need to move battery_task.py code here and do additional handling for bad circumstances that the cubesat should react to.
polling various values to direct satellite operating modes. monitors batteries, temps, and current.
    has elements of battery-task BUT has various thresholds for payload operation.

* Author: Caden Hillis
"""

from Tasks.template_task import Task
import time

class task(Task):
    priority = 2
    frequency = 1/10
    name = 'housekeeper'
    color = 'orange'

    async def main_task(self):

        #print values of interest:
        self.debug("Voltage of battery = " + str(self.cubesat.battery_voltage)  + " Threshold = " + str(self.cubesat.vlowbatt))
        self.debug("Battery charge current = NOT IMPLEMNTED")
        self.debug("Bus current = " + str(self.cubesat.current_draw))
        self.debug("USB charging = " + str(self.cubesat.usb_charging))
        self.debug("Solar charging = " + str(self.cubesat.solar_charging))