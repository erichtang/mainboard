
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
        'no-op':        db_cdh.noop,
        'hreset':       db_cdh.hreset,
        'query':        db_cdh.query,
        'exec_cmd':     db_cdh.exec_cmd,
        # new
        'get_imu_offset': db_cdh.get_imu_offset,
        'write':        db_cdh.write
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

        #self.debug("usb console task")

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
                rx = rx.decode('utf-8')
                rx = rx.replace('\r', '')
                rx = rx.split(' ', 1)
                try:  cmd =  rx[0]
                except: cmd = None
                try: args = rx[1].split(",")
                except: args=None
                if cmd is not None:
                    if args is None:
                        db_cdh.write(co('running {} (without args)'.format(cmd), 'orange'))
                        try:
                            self.db_cmd_dispatch[cmd](self)
                        except KeyError:
                            db_cdh.write(co('invalid command', 'red', 'bold'))
                        except Exception as e:
                            db_cdh.write(co('valid command, but execution failed: {}'.format(e), 'red', 'bold'))
                    else:
                        db_cdh.write(co('running {} (with args: {})'.format(cmd,args), 'orange'))
                        try:
                            self.db_cmd_dispatch[cmd](self, args)
                        except KeyError:
                            db_cdh.write(co('invalid command', 'red', 'bold'))
                        except Exception as e:
                            db_cdh.write(co('valid command, but execution failed: {}'.format(e), 'red', 'bold'))
            usb_cdc.data.write(bytes(">>>", 'utf-8'))
            
