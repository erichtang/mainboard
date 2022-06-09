"""
Garbage collection task

"""
from Tasks.template_task import Task
import gc

class task(Task):
    priority = 1
    frequency = 1
    name='gc_task'
    color = 'pink'

    async def main_task(self):
        #before = [gc.mem_alloc(), gc.mem_free()]
        gc.collect()
        after = [gc.mem_alloc(), gc.mem_free()]
        #self.debug('Before the garbage man came:')
        #self.debug('{} bytes allocated, {} bytes free'.format(before[0], before[1]), 2)
        self.debug('After the garbage man came:')
        self.debug('{} bytes allocated, {} bytes free'.format(after[0], after[1]), 1)
        

