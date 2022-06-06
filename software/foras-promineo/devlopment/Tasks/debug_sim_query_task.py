
"""

"""
from Tasks.template_task import Task
import db_cdh
from debugcolor import co
import usb_cdc


class task(Task):
    priority = 1
    frequency = 100 # 1Hz
    name='simulation_query'
    color = 'red'
    timeout = 10 #10ms

    schedule_later = False


    """
    values it will ask the host PC if it is simulating. 
    Host PC will respond with what will be simulated
    """
    simulated_values_bools = {
        "value1": True
        "value1": False
        "value1": False
        "value1": True
    }


    def __init__(self,satellite):
        super().__init__(satellite)
        usb_cdc.data.reset_input_buffer
        usb_cdc.data.timeout = 0.1
        db_cdh.write("\r\n-----------------------------------------------------------")
        db_cdh.write(co("Debug USB Channel OPEN ! :)", 'green', 'bold'))
        db_cdh.write("-----------------------------------------------------------")
        usb_cdc.data.write(bytes(">>>", 'utf-8'))

    async def main_task(self):
        #ask for updated byte
        #if no response it will move on and assert to not simulated
        pass