
"""
uses the usb_cdc.data USB channel as an interface for recieving commands from the host-pc.
        #TODO work on simulation interface

Author: C.Hillis
"""
from Tasks.template_task import Task
import db_cmds 
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
            db_cmds.write('INIT')

        #TODO this shall also change to be single byte command codes for recieveing.
        self.dispatch = { # TODO update this dictionary IN ORDER of cmds in db_cdh.py.
        'noop':                db_cmds.noop,
        'hreset':               db_cmds.hreset,
        'query':                db_cmds.query,
        'exec_cmd':             db_cmds.exec_cmd,
        'write':                db_cmds.write,
        'i2c_scan':             db_cmds.i2c_scan,
        'print_gyro':           db_cmds.print_gyro,
        'print_mag':            db_cmds.print_mag,
        'print_accel':          db_cmds.print_accel,
        'download_logfile':     db_cmds.download_logfile,
        'upload':               db_cmds.upload,
        'download':             db_cmds.download,
        'sd_rm'    :            db_cmds.sd_rm,
        'simulate':             db_cmds.simulate,
        'pl_noop' :             db_cmds.pl_noop,
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
                if header[1] > 3: #header size is 3
                    #get data if it exists
                    rx = usb_cdc.data.read(header[1])

                #write code to compute checksum rx[2]
                self.debug(header)
                if header[0:1] in db_cmds.rx:
                    # execute cmd with no args
                    if rx is None:
                        try:
                            # self.debug(db_cmds.rx[header[0:1]])
                            self.dispatch[db_cmds.rx[header[0:1]]](self)
                            
                        except Exception as e:
                            
                            db_cmds.write('ERROR', str(e))
                    # execute cmd with args
                    else:
                        try:
                            self.dispatch[db_cmds.rx[header[0:1]]](self, rx)
                        except Exception as e:
                            db_cmds.write('ERROR', str(e))
                else:
                    db_cmds.write('ERROR', 'invalid cmd code')