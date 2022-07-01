"""
Garbage collection task

Author: C.Hillis
"""
from Tasks.template_task import Task
import gc

class task(Task):
    priority = 4
    frequency = 1
    name='gc'
    color = 'pink'

    async def main_task(self):
        #before = [gc.mem_alloc(), gc.mem_free()]
        gc.collect()
        after = [gc.mem_alloc(), gc.mem_free()]

        self.debug('{} bytes allocated, {} bytes free'.format(after[0], after[1]))
        

