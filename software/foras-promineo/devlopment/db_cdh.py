"""
TODO -- complete empty functions definitions
            think of more possible commands to add for future debugging.
USB debug commands from the cubesat host-pc.

Author: C. Hillis
"""
import time
import os
import usb_cdc
from debugcolor import co

########### commands without arguments ###########
##################################################
def noop(self):
    """
    A no-op command.

    Returns:
        'ACK'
    """
    write(co('ACK', 'green'))

def hreset(self):
    """
    Hard resets the MCU. (Powers off and on again)

    Returns:
        Success: Board re-initalization
        Failure: 'Reset Failed'
    """
    write('Resetting')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        write('Reset Failed')

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
        write('Execution failed... : {}'.format(e))

def print_gyro(self):
    """
    prints gyroscope data.
    """
    write("gyro0 : {}".format(self.cubesat.imu.gyro0))
    write("gyro1 : {}".format(self.cubesat.imu.gyro1))
    write("gyro2 : {}".format(self.cubesat.pib.imu.gyro0))
    write("gyro3 : {}".format(self.cubesat.pib.imu.gyro1))

def print_mag(self):
    """
    prints magnetometer data.
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

def print_chunks_test(self):
    #temporary file print test function. prints file data in 256 byte chunks so this code can be portable to the radio and payload interface with minor modifications...
    chunk_size = 256
    length = os.stat(self.cubesat.logfile)[6]
    with open(self.cubesat.logfile, "rb") as f:
        write("Printing Logfile. Length {} bytes. {} {} byte packets".format(length, chunk_size, int(length/240)))
    
        write("FILE_START:")
        while True:
            chunk = f.read(chunk_size)
            if chunk == b"":
                break
            usb_cdc.data.write(chunk)
        write(":FILE_END")
        
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
    TODO -- not tested.
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
        part :: path to the file. :/sd/ is added to the front.
    
    Returns:
        a file
            start string "FILE_START:"
            end string ":FILE_END\r\n"
            bytes data. encoding is dependent on file.
    """
    if path[:4] != "/sd/":
        path = "/sd/" + path
    chunk_size = 256
    length = os.stat(path)[6]
    write("Printing {}. Length {} bytes. {} {} byte packets".format(path, length, chunk_size, int(length/240)))
    with open(path, "rb") as f:
        usb_cdc.data.write("FILE_START:".encode('utf-8'))
        while True:
            chunk = f.read(chunk_size)
            if chunk == b"":
                break
            usb_cdc.data.write(chunk)
        usb_cdc.data.write(':FILE_END\r\n'.encode('utf-8'))
        f.close()
    pass

def sd_rm(self, path):
    """
    TODO -- not implimented
    deletes a fole from SD

    Paramaters:
        path :: path to the file. :/sd/ is added to the front.
    
    Returns:
        None
    """
    pass

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

def write(msg):
    """
    writes a string to usb_cdc.data
    appends \r\n tp passed string.
    """
    msg = msg + '\r\n'
    usb_cdc.data.write(bytes(msg, 'utf-8'))

def waitforinput():
    """
    waits for ANY input then throws the data away
    useful for pib verification
    i think this function can go away soon...
    """
    write("Press enter to continue")
    waitflag = True
    while waitflag:
        if usb_cdc.data.in_waiting:
            rx = usb_cdc.data.readline()
            if rx:
                waitflag = False
        time.sleep(1)