
"""
uses the usb_cdc.data USB as an interface for recieving commands from the host-pc.
        polls the usb_cdc.data channel actively for new utf-8 encoded commands and args.
        #TODO working on file tx/rx that will NOT be utf-8 encoded but that is TBR

all references to usb_cdc DATA are kept within this task. other files in this repository SHALL NOT reference usb_cdc.data at all.

Author: C.Hillis
"""
from Tasks.template_task import Task
import db_cdh 
from debugcolor import co
import usb_cdc


class task(Task):
    priority = 1
    frequency = 1 # 1Hz
    name='usb_debug'
    color = 'blue'

    schedule_later = False

    

    def __init__(self,satellite):
        self.cubesat = satellite

        usb_cdc.data.reset_input_buffer
        usb_cdc.data.timeout = 0.1
        if usb_cdc.data.connected:
            db_cdh.write("\r\n-----------------------------------------------------------")
            db_cdh.write(co("Debug USB Channel OPEN ! :)", 'green', 'bold'))
            db_cdh.write("-----------------------------------------------------------")
            usb_cdc.data.write(bytes(">>>", 'utf-8'))

        self.dispatch = { # TODO update this dictionary IN ORDER of cmds in db_cdh.py.
        'no-op':                db_cdh.noop,
        'hreset':               db_cdh.hreset,
        'query':                db_cdh.query,
        'exec_cmd':             db_cdh.exec_cmd,
        'write':                db_cdh.write,
        'i2c_scan':             db_cdh.i2c_scan,
        'print_gyro':           db_cdh.print_gyro,
        'print_mag':            db_cdh.print_mag,
        'print_accel':          db_cdh.print_accel,
        'print_chunks_test':    db_cdh.print_chunks_test,
        'download_logfile':     db_cdh.download_logfile,
        'upload':               db_cdh.upload,
        'download':             db_cdh.download,
        'simulate':             db_cdh.simulate
    }

    async def main_task(self):
        
        """
        Checks if there are any commands in waiting.

        cmd structure:
        all commands will be terminated with \n (i.e. a single line and \r is optional), ASCII encoded
        all args passed shall be separated with "," NOT ", "
        """
        if usb_cdc.data.connected:
            """
            If usb_cdc.data is connected, it looks for commands and data
            """
            heard_cmd = usb_cdc.data.in_waiting
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
                                self.dispatch[cmd](self)
                            except KeyError:
                                db_cdh.write(co('invalid command', 'red', 'bold'))
                            except Exception as e:
                                db_cdh.write(co('valid command, but execution failed: {}'.format(e), 'red', 'bold'))
                        else:
                            db_cdh.write(co('running {} (with args: {})'.format(cmd,args), 'orange'))
                            try:
                                self.dispatch[cmd](self, args)
                            except KeyError:
                                db_cdh.write(co('invalid command', 'red', 'bold'))
                            except Exception as e:
                                db_cdh.write(co('valid command, but execution failed: {}'.format(e), 'red', 'bold'))
                usb_cdc.data.write(bytes(">>>", 'utf-8'))
        else:
            """
            if usb_cdc.data is NOT connected this task sets self.simulate values to False
            """
            for value in self.cubesat.sim.simulate:
                value = False
