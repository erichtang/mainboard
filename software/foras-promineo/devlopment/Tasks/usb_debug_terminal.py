
"""
usb debug task thru usb_cdc lib called in boot.py

uses the usb_cdc DATA usb comms, not the CONSOLE used by the REPL

all references to usb_cdc DATA are kept within this task so it can be easily removed/ignored for flight software

"""
from Tasks.template_task import Task
import cdh
import db_cdh
from debugcolor import co

class task(Task):
    priority = 3
    frequency = 1 # 1Hz
    name='usb_debug'
    color = 'purple'

    schedule_later = True

    db_cmd_dispatch = {
        #ota command copies
        'no-op':        db_cdh.noop,
        'hreset':       db_cdh.hreset,
        'query':        db_cdh.query,
        'exec_cmd':     db_cdh.exec_cmd,
        # new, db only commands
        'get_imu_offset': db_cdh.get_imu_offset,
    }


    def __init__(self,satellite):
        super().__init__(satellite)

    async def main_task(self):

        heard_cmd = await usb_cdc.data.in_waiting()

        """
        cmd structure:
        all commands will ne terminated with \n (i.e. a single line), ASCII encoded
        all args passed shall be separated with "," NOT ", "
        """
        if heard_cmd:
            
            rx = usb_cdc.data.readline() 

            #parse data until first space and correlate that to command
            cmd = []
            args = []
            for letter in rx:
                if rx[letter] == " ":
                    cmd = rx[:letter-1]
                    args = rx[letter+1:]

            if cmd is None:
                usb_cdc.data.write(co("cmd not detected :(", "red", "bold"))

            usb_cdc.data.write("do debug cdh handle here", cmd, args)

            if cmd in self.db_cmd_dispatch:
                try:
                    if args is None:
                        usb_cdc.data.write('running {} (no args)'.format(cmd))
                        self.db_cmd_dispatch[cmd](self)
                    else:
                        usb_cdc.data.write('running {} (with args: {})'.format(cmd,args))
                        self.db_cmd_dispatch[cmd](self,args)
                except Exception as e:
                    usb_cdc.data.write(co('something went wrong: {}'.format(e), 'red'))
            else:
                usb_cdc.data.write('invalid command!')

                
