"""
healthcheck_task.py



"""


from Tasks.template_task import Task

class task(Task):
    priority = 4
    frequency = 1/10 # once every 10s
    name = 'test'
    color = 'pink'

    schedule_later = True

    async def main_task(self):
        self.debug('System Health Task')
        #self.cubesat.print_file(self.cubesat.logfile) # why does this b weird
        
