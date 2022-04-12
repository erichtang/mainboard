
"""
usb debug task thru usb_cdc lib called in boot.py

uses the usb_cdc DATA usb comms, not the CONSOLE used by the REPL

all references to usb_cdc DATA are kept within this task so it can be easily removed/ignored for flight software

"""
from Tasks.template_task import Task
import db_cdh
from debugcolor import co
import usb_cdc


class task(Task):
    priority = 3
    frequency = 1 # 1Hz
    name='usb_debug'
    color = 'blue'

    schedule_later = True

    db_cmd_dispatch = {
        #ota command copies
        bytes('no-op', 'utf-8'):        db_cdh.noop,
        'hreset':       db_cdh.hreset,
        'query':        db_cdh.query,
        'exec_cmd':     db_cdh.exec_cmd,
        # new, db only commands
        'get_imu_offset': db_cdh.get_imu_offset,
    }


    def __init__(self,satellite):
        super().__init__(satellite)
        usb_cdc.data.reset_input_buffer
        usb_cdc.data.timeout = 0.1
        usb_cdc.data.write(bytearray(co("\nDebug USB Channel OPEN ! :)\r\n", 'green', 'bold')))

    async def main_task(self):

        self.debug("usb console task")

        heard_cmd = usb_cdc.data.in_waiting

        """
        cmd structure:
        all commands will ne terminated with \n (i.e. a single line), ASCII encoded
        all args passed shall be separated with "," NOT ", "
        """

        rx=None
        if heard_cmd >= 1:
            rx = usb_cdc.data.readline()
            if rx is not None:
                #parse data until first space
                cmd = []
                args = []
                for letter in range(len(rx)):
                    if rx[letter] == " ":
                        cmd = rx[:letter]
                        args = rx[letter:]
                        break
                #finding command in cmd_dispatch dict
                #args = str(args, 'utf-8')
                usb_cdc.data.write(bytes(co('command: {}\r\n args: {}\r\n'.format(cmd, args), 'orange'), 'utf-8'))
                try:
                    cmd = self.db_cmd_dispatch[cmd]
                except KeyError:
                    usb_cdc.data.write(bytes(co('invalid command\r\n', 'red', 'bold')))
                    cmd = None
                except Exception as e:
                    usb_cdc.data.write(bytes(co('something went wrong: {}\r\n'.format(e), 'red', 'bold'), 'utf-8'))
                    cmd = None
                #if it found something
                if cmd is not None:
                    usb_cdc.data.write(bytes(co("cmd not detected :(\r\n", "red", "bold")))
                    if args is None:
                        usb_cdc.data.write(bytes('running {} (no args)\r\n'.format(cmd)))
                        try:
                            cmd(self)
                        except Exception as e:
                            usb_cdc.data.write(bytes(co('command execution failed\r\n'.format(cmd), 'red', 'bold')))
                    else:
                        usb_cdc.data.write(bytes('running {} (with args: {})\r\n'.format(cmd,args)))
                        try:
                            cmd(self,args)
                        except Exception as e:
                            usb_cdc.data.write(bytes(co('command execution failed\r\ncmd: {}\r\nargs:{}'.format(cmd, args), 'red', 'bold')))
                self.debug("End usb db terminal task")
            
