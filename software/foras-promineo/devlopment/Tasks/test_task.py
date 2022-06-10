"""
this task is just a task that can test out functions in devlopment and other things
changes frequently for what needs testing.

* Author: Caden Hillis
"""
from Tasks.template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1 # once every 10s
    name = 'test'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        pass