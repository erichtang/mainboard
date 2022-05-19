"""
NOT DONE
this task is just a task that can test out functions in devlopment and other things
changes frequently for what needs testing.
"""
from Tasks.template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1/10 # once every 10s
    name = 'test'
    color = 'gray'

    schedule_later = True

    async def main_task(self):
        self.debug('test start: {}'.format(time.monotonic()))
        #print imu data
        for imu_type in self.cubesat.data_cache['imu']:
            self.debug('{:>5} {}'.format(imu_type,self.cubesat.data_cache['imu'][imu_type]),2)

        #await self.cubesat.tasko.sleep(10)
        self.debug('test stop: {}'.format(time.monotonic()))
