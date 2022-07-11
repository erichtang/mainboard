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
    name = 'power monitor'
    color = 'orange'

    d_cfg = {
        'priority' : 2,
        'frequency' : 1/10,
    }

    async def main_task(self):

       # check temps
       pass