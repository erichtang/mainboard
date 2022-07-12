
"""
uses the usb_cdc.data USB as an interface for recieving commands from the host-pc.
        polls the usb_cdc.data channel actively for new commands/
        #TODO working on file tx/rx that will NOT be utf-8 encoded but that is TBR
        #TODO work on simulation interface

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
            db_cdh.write('INIT')

        #TODO this shall also change to be single byte command codes for recieveing.
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
        'download_logfile':     db_cdh.download_logfile,
        'upload':               db_cdh.upload,
        'download':             db_cdh.download,
        'sd_rm'    :            db_cdh.sd_rm,
        'simulate':             db_cdh.simulate
    }

    async def main_task(self):
        
        """
        Checks if there are any commands in waiting.

        cmd structure:
        3 byte header:
            1 byte cmd code
            1 byte msg len
            1 byte checksum
        x bytes of msg
        """
        if usb_cdc.data.connected:
            """
            If usb_cdc.data is connected, it looks for commands and data
            """
            #listen for command
            rx=None
            heard_cmd = usb_cdc.data.in_waiting
            if heard_cmd >= 1:
                # get header
                header = usb_cdc.data.read(3)
                if header[1] > 0:
                    #get data if it exists
                    rx = usb_cdc.data.read(header[1])

                #write code to compute checksum rx[2]

                if header[0] in db_cdh.rx:
                    # execute cmd with no args
                    if rx is None:
                        try:
                            self.dispatch[db_cdh.rx[header[0]]](self)
                        except Exception as e:
                            db_cdh.write('ERROR', str(e))
                    # execute cmd with args
                    else:
                        try:
                            self.dispatch[db_cdh.rx[header[0]]](self, rx)
                        except Exception as e:
                            db_cdh.write('ERROR', str(e))
                else:
                    db_cdh.write('ERROR', 'invalid cmd code')