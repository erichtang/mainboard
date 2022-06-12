"""
PIB tester task. Just for PIB verification and testing

"""
from Tasks.template_task import Task
import gc
import time

class task(Task):
    priority = 2
    frequency = 1/10
    name='pib tester'
    color = 'red'

    async def main_task(self):

        gc.collect()

        self.debug("Reading CH 0")
        self.cubesat.pib.adc.ch0_en = True
        self.debug("CH 0 Setting: {}".format(self.cubesat.pib.adc.ch0_en))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.cubesat.pib.adc.ch0_en = False

        self.debug("Reading CH 1")
        self.cubesat.pib.adc.ch1_en = True
        self.debug("CH 1 Setting: {}".format(self.cubesat.pib.adc.ch1_en))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.cubesat.pib.adc.ch1_en = False

        self.debug("Reading CH 2")
        self.cubesat.pib.adc.ch2_en = True
        self.debug("CH 2 Setting: {}".format(self.cubesat.pib.adc.ch2_en))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.cubesat.pib.adc.ch2_en = False

        self.debug("Reading CH 3")
        self.cubesat.pib.adc.ch3_en = True
        self.debug("CH 3 Setting: {}".format(self.cubesat.pib.adc.ch3_en))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.debug("ADC Reading: {}".format(self.cubesat.pib.adc.read))
        self.cubesat.pib.adc.ch3_en = False


