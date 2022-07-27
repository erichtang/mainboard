from adcs import ADCS

"""
TODO: ADCS code needs to be ported from C.

Attidude control conops are quite complex and need to be defined simpy here.

FSM running all attitude control related data handling and execution
"""

from Tasks.template_task import Task
import time
class task(Task):

    name = 'adcs'

    d_cfg = {
        'priority' : 2,
        'frequency' : 1,
    }

    def __init__(self):
        super().__init__('Task')
        self.adcs = ADCS(self.cubesat)

    async def main_task(self):
        self.adcs.processADCSevents()
