"""
controls the onboard neopixel RGB LED on the mainboard.

TODO I want to change this to be a rainbow
"""

from Tasks.template_task import Task

class task(Task):
    priority = 255
    frequency = 10 
    name='blink'
    color = 'pink'

    rgb_on = False

    async def main_task(self):
        #self.debug("blinky :)")
        if self.rgb_on:
            self.cubesat.RGB=(0,0,0)
            self.rgb_on=False
        else:
            self.cubesat.RGB=(0,255,0)
            self.rgb_on=True



