from Tasks.template_task import Task
import time

class task(Task):
    priority = 1
    frequency = 5
    name = 'test'

    need_to_check = True

    async def main_task(self):
        # need to fix so it remembers forever once deployeed, write to a fix on the sd
        if self.need_to_check:
            if (time.time() - self.cubesat.BOOTTIME)/60 > self.cubesat.minutes_to_wait:
                self.need_to_check = False
            else:
                return

        print("here")
        time.sleep(10)
        