from Tasks.template_task import Task
import time

class task(Task):
    
    
    def __init__(self, satellite):

        self.cubesat = satellite

        #change all other task settings for payload mode

    async def main_task(self):
        """
        main payload loop

        
        """