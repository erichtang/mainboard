"""
TODO -- complete empty functions definitions
            think of more possible commands to add for future debugging.
TODO -- all of the write() responses need to be re-wrote
USB debug commands from the cubesat host-pc. commands are called from usb_debug_task.py's distpatch{} dict

Author: C. Hillis
"""
import time
import os

# from numpy import isin
import usb_cdc
from debugcolor import co
import payload_cmds

rx = { # recieved codes from host PC
    b'\x00' : 'noop',
    b'\x07' :'hreset',
    b'\x02' : 'sreset',
    b'\x03' : 'i2c_scan',
    b'\x04' : 'print_gyro',
    b'\x05' : 'print_mag',
    b'\x06' : 'print_accel',
    b'\x01' : 'pl_noop',
    b'\x08' : 'pl_cmd_photo',
    b'\x09' : 'sd_ls',
    b'\x0a' : 'download_logfile',
    b'\x0b' : 'print_mainboard_telemtery',
    b'\x0c' : 'print_payload_telemtery',
    b'\x0d' : 'print_pib_telemetry',
    b'\x0e' : 'print_startracker_telemetry',
    b'\x0f' : 'print_adcs_telemetry',
    b'\x10' : 'print_pwr_telemetry',
    b'\x11' : 'print_temperature_telemetry',
    b'\x12' : 'print_state_telemetry',
    b'\x13' : 'print_time',
    b'\x14' : 'query',
    b'\x15' : 'exec_cmd',
    b'\x16' : 'stop_task',
    b'\x17' : 'start_task',
    b'\x18' : 'change_task_priority',
    b'\x19' : 'change_task_frequency',
    b'\x1a' : 'configure_file',
    b'\x1b' : 'upload',
    b'\x1c' : 'download',
    b'\x1d' : 'sd_rm',
    b'\x1e' : 'pl_cmd_arm',
    b'\x1f' : 'usb_cmd_payload_photo_burst',
    b'\x20' : 'pl_cmd',
    b'\x21' : 'simulate',
    b'\x22' : 'crc_file',
    b'\x23' : 'radio_cmd',
    b'\x24' : 'deploy_antenna',
    b'\x25' : 'write',
    b'\x26' : 'pl_cmd_hreset' ,
    b'\x27' : 'pl_cmd_sreset' ,
}

tx = { # transmitted to host PC
    'ACK'           : b'\x00',
    'INIT'          : b'\x01',
    'NACK'          : b'\xff',
    'ERROR'         : b'\xf0',
    'BURST_ST'      : b'\xb0',
    'BURST_DATA'    : b'\xbd',
    'BURST_END'     : b'\x0b',
    'CMD_RESPONSE'  : b'\xe5' #general command response code, like for print commands.
}

########### commands without arguments ###########
##################################################

def noop(self):
    """
    A no-op command.

    Returns:
        'ACK'
    """

    # f = open('Tasks/testfile.txt', "w")
    # f.write("This is a test")
    # f.close()

    write('ACK')

def hreset(self):
    """
    Hard resets the MCU. (Powers off and on again)

    Returns:
        Success: Board re-initalization
        Failure: 'Reset Failed'
    """
    write(self, 'CMD_RESPONSE', 'resetting...')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        write(self, 'NACK')

def sreset(self):
    """
    TODO -- not implemented
    Soft reset of the MCU (no power cycle)

    Returns:
        Success: Board re-initalization
        Failure: "Reset Failed"
    """

def i2c_scan(self):
    """
    i2c device scan

    prints detected i2c devices.
    """
    while not self.cubesat.i2c1.try_lock():
        pass
    try:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in self.cubesat.i2c1.scan()],
        )
    except Exception as e:
        write(self, 'ERROR', 'Execution failed... : {}'.format(e))

def print_gyro(self):
    """
    TODO change
    prints gyroscope data.
    """
    write("gyro0 : {}".format(self.cubesat.imu.gyro0))
    write("gyro1 : {}".format(self.cubesat.imu.gyro1))
    write("gyro2 : {}".format(self.cubesat.pib.imu.gyro0))
    write("gyro3 : {}".format(self.cubesat.pib.imu.gyro1))

def print_mag(self):
    """
    TODO change
    """
    write("mag0 : {}".format(self.cubesat.imu.mag0))
    write("mag1 : {}".format(self.cubesat.imu.mag1))
    write("mag2 : {}".format(self.cubesat.pib.imu.mag0))
    write("mag3 : {}".format(self.cubesat.pib.imu.mag1))

def print_accel(self):
    """
    prints accelerometer data.
    """
    write("accel0 : {}".format(self.cubesat.imu.accel0))
    write("accel1 : {}".format(self.cubesat.imu.accel1))
    write("accel2 : {}".format(self.cubesat.pib.imu.accel0))
    write("accel3 : {}".format(self.cubesat.pib.imu.accel1))

def sd_ls(self):
    """
    TODO -- not implemented
    lists folders and files on the SD card.
    """
    pass
        
def download_logfile(self):
    """
    prints the logfile to the terminal. the host-pc software should take this data and output a file a user can read.

    Returns:
        see download_from_sd def.
    """
    download(self, self.cubesat.logfile)

def print_mainboard_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionary of values for the mainboard telemetry.

    Returns:
        TBR
    """
    pass

def print_payload_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionary of values for the payload telemetry.

    Returns:
        TBR
    """
    pass

def print_pib_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionary of values for the pib telemetry.

    Returns:
        TBR
    """
    pass

def print_startracker_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionary of values for the startracker telemetry.

    Returns:
        TBR
    """
    pass

def print_adcs_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionary of values for the adcs telemetry.

    Returns:
        TBR
    """
    pass

def print_pwr_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionay of values for the satellite power telemetry.

    Returns:
        TBR
    """
    pass

def print_temperature_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionay of values for the satelite temperature telemetry.

    Returns:
        TBR
    """
    pass

def print_state_telemetry(self):
    """
    TODO -- not implemented
    prints a dictionay of values for the task execution states of the satellite.


    Returns:
        TBR
    """
    pass

def print_time(self):
    """
    TODO -- not implemented
    prints time in GMT

    Returns:
        TBR
    """
    pass

########### commands with arguments ###########

def query(self,args):
    """
    runs python method eval(args)

    Prints:
        Success: results of eval
        Failure: exeception / error
    """
    write('query: {}'.format(args))
    try:
        write(eval(bytes(args,'utf-8')))
    except Exception as e:
        write('Evaluation failed... : {}'.format(e))

def exec_cmd(self,args):
    """
    runs python method eval(args)

    Returns:
        Success: nothing 
        Failure: exeception / error
    """
    arg = args[0]
    write('exec: {}'.format(arg))
    try:
        exec(bytes(arg, 'utf-8'))
    except Exception as e:
        write('Execution failed... : {}'.format(e))

def stop_task(self, task): 
    """
    TODO -- Not implemented
    stops task

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict

    Returns:
        None
    """
    pass

def start_task(self, task): 
    """
    TODO -- not implemented
    starts task

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict

    Returns:
        None
    """
    pass

def change_task_priority(self, task):
    """
    TODO -- not implimented
    changes task priority

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict
    
    Returns:
        None
    """
    pass

def change_task_frequency(self, task):
    """
    TODO -- not implemented
    changes task frequency

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict
    
    Returns:
        None
    """
    pass

def configure_file(self, name, *kwargs):
    """
    TODO -- not implimented
    overwrites config file (dictionary) with provided kwargs

    Paramaters:
        name    :: the name of the .bak config file
        *kwargs :: keyword / argument pairs for this config file's dictionary.
                        refer to the declaration of each config
    
    Returns:
        None
    """
    pass

def upload(self, path):
    """
    TODO -- not tested. -- doesnt work. use def download as a good example for upload.
    adds a file of name to the path specified on the sd.
        this is a special command, as the file must be passed AFTER th \r\n of the original cmd and args!! this 

    Paramaters:
        path :: the file locaton. /sd/ added to begining location
    
    Returns:
        None
    """
    to = usb_cdc.data.timeout
    usb_cdc.data.timeout = .1

    if path[:4] != "/sd/":
        path = "/sd/" + path

    chunk_size = 256
    with open(path, 'ab') as f:
        while True:
            waiting = usb_cdc.data.in_waiting
            if waiting < chunk_size:
                f.write(usb_cdc.data.read(waiting))
                break
            else:
                f.write(usb_cdc.data.read(chunk_size))
        f.close()
    usb_cdc.data.timeout = to

    write("File uploaded to {}".format(path))
    write("To verify file integrety, execute cmd crc_file.")

def download(self, path):
    """
    sends a file to the host-pc specified by the path provided

    Paramaters:
        utf-8 encoded string of the path to the file. /sd/ is added to the front.
    
    Returns:
        BURST_ST CMD
            [0:3] 4 byte integer of number of bytes
            [4:5] 2 byte integer of number of chunks

        BURST_DATA CMD
            [0:252] this chunk of data.

        BURST_END_CMD
    """
    #get path
    if isinstance(path, bytearray):
        path = path.decode('utf-8')
    if path[:4] != "/sd/":
        path = "/sd/" + path
    
    #send start
    chunk_size = 253
    length = os.stat(path)[6] 
    chunks = int(length / chunk_size)
    start_msg = bytearray(6)
    start_msg[0:3] = length.to_bytes(4, 'big')
    start_msg[4:5] = chunks.to_bytes(2, 'big')
    write(self, 'BURST_ST', start_msg)

    #send chunks
    with open(path, "rb") as f:
        while True:
            write(self, 'BURST_DATA', f.read(chunk_size))
            chunks -= 1
            if chunks <= 0: break
        f.close()
    
    #send end cmd
    write(self, 'BURST_END')


def sd_rm(self, path):
    """
    TODO -- not implimented
    deletes a fole from SD

    Paramaters:
        path :: path to the file. :/sd/ is added to the front.
    
    Returns:
        None
    """
    write(path[0])
    os.remove(path[0])

def pl_noop(self):
    """
    TODO -- WIP psudeocode only
    sends no-op command to payload, waits for ACK, then sends ACK to host PC, if no ACK is rx'd in 1 second, this command will send NACK to the host pc.
    
    Returns ACK or NACK
    """
    self.debug('dbcmds')
    if payload_cmds.noop(self):
        #TOD write code here to respond ACK
        
        
        write('ACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    else:
        
        write('NACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    # time.sleep(2)
    # if payload_cmds.testnoop(self):
    #     #TOD write code here to respond ACK
        
        
    #     write('ACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    # else:
        
    #     write('NACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE

def pl_cmd_hreset(self):
    if payload_cmds.hreset(self):
        #TOD write code here to respond ACK
        
        
        write('ACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    else:
        
        write('NACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE

def pl_cmd_sreset(self):
    """
    TODO -- WIP psudeocode only
    sends soft reset command to payload, waits for ACK, then sends ACK to host PC, if no ACK is rx'd in 1 second, this command will send NACK to the host pc.
    
    Returns ACK or NACK
    """
    if payload_cmds.sreset(self):
        #TOD write code here to respond ACK
        
        
        write('ACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    else:
        
        write('NACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    # time.sleep(2)
    # if payload_cmds.testnoop(self):
    #     #TOD write code here to respond ACK
        
        
    #     write('ACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE
    # else:
        
    #     write('NACK') # THIS NEEDS TO CONFORM TO NEW HEADER STRUCTURE



def pl_cmd_arm(self, *args):
    """
    TODO -- not implimented
    payload arm command. sends command to the payload of paramaters given

    Paramaters:
        *args :: mainboard <-> payload UART interface has yet to be defined.
    
    Returns:
        None
    """
    pass



def usb_cmd_payload_photo_burst(self):

    self.debug('usbcmdpldphbrst')


    self.cubesat.source = 'payload'
    self.cubesat.destination = 'usb'
    self.cubesat.burst_f = True
    self.cubesat.chunk_i = 0
    self.cubesat.buffer_ready_f = False
    self.cubesat.chunk_t = payload_cmds.request_photo_size(self)    #????\

    self.debug(self.cubesat.chunk_t)

    # self.cubesat.chunk_t = payload_cmds.request_photo_size(self)    #????\
    self.cubesat.scheduled_tasks['burst_transfer'].start()



    

def pl_cmd_photo(self, *args):
    """
    TODO -- not implimented
    payload photo command. sends command to the payload of paramaters given

    Paramaters:
        *args ::  mainboard <-> payload UART interface has yet to be defined.
    
    Returns:
        None
    """
    pass

def pl_cmd(self, *args):
    """
    TODO -- not implimented
    payload command. sends command to the payload of paramaters given

    Paramaters:
         *args ::  mainboard <-> payload UART interface has yet to be defined.
    
    Returns:
        None
    """
    pass

def simulate(self, *args):
    """
    TODO -- ignore this while i work out simualation kinks
    simulate command. 

    Paramaters:
        passed args are keys in the self.cubesat.sim.simulate dict
        they TOGGLE simulation

    Returns:
        TBR
    """
    for arg in args:
        if arg in self.cubesat.sim.simulate:
            self.cubesat.sim.simulate[arg] = not self.cubesat.sim.simulate[arg]
            write("Simulation for value: {} set  to {}" .format(arg, str(self.cubesat.sim.simulate[arg])))

def crc_file(self, path, crc):
    """
    TODO -- not implimented
    computates a crc-32 checksum for the file at the given path and compares it with the crc provided.

    Paramaters:
        path :: path to file
        crc  :: crc-32 checksum
    
    Returns:
        TBR
    """
    pass

def radio_cmd(self, cmd, *kwargs):
    """
    TODO -- not implimented
    preforms radio command with given kwargs passed

    Paramaters:
        cmd :: the name of the command as seen in the cdh.dispatch dict.
        *kwargs :: keyword arguments (if any) passed.
    
    Returns:
        None
    """
    pass

def deploy_antenna(self):
    """
    TODO -- not implimented
    preforms antenna deployment.
    """
    pass
########### helper functions for using usb_cdc.data ###########

def write(cmd, data=None):
    """
    writes a formatted message over usb_cdc.data to the host PC
    """


    if data is None:
        length = 0
    else:
        length = len(data)
    
    msg = bytearray(3+length)
    msg[0] = tx[cmd][0]
    msg[1] = length
    msg[2] = 0
    if length > 0:
        if not isinstance(data, bytearray) and not isinstance(data, bytes) and not isinstance(data, memoryview):         #why needed?
            data = data.encode('utf-8')
        msg[3:] = data
    #     print(data)
    # print(msg)
    # for i in range(length + 3):
    #     print(i)
    #     print( msg[i])
    usb_cdc.data.write(msg)
    # print('write !!!!!!!!!!!!!!!!!!!!!!!!:')
    # print(msg)
