import time
import usb_cdc
from debugcolor import co

########### commands without arguments ###########
def noop(self):
    """
    A no-op command.

    Returns:
        "ACK"
    """
    write(co('ACK', 'green'))

def hreset(self):
    """
    Hard resets the MCU. (Powers off and on again)

    Returns:
        Success: Board initalization prints on both terminals
        Failure: "Reset Failed"
    """
    write('Resetting')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        write('Reset Failed')

def sreset(self):
    """
    TODO
    Soft reset of the MCU (no power cycle)

    Returns:
        Success: Board initalization prints on both terminals
        Failure: "Reset Failed"
    """

def i2c_scan(self):
    """
    TODO
    i2c device scan

    Returns:
        detected i2c devices
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

def sd_ls(self):
    pass

def download_log(self):
    pass

########### commands with arguments ###########

def query(self,args):
    """
    runs python method eval(args)

    Returns:
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
    TODO 
    stops task

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict

    Returns:
        None
    """
    pass

def start_task(self, task): 
    """
    TODO 
    starts task

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict

    Returns:
        None
    """
    pass

def change_priority(self, task):
    """
    TODO
    changes task priority

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict
    
    Returns:
        None
    """
    pass

def change_frequency(self, task):
    """
    TODO
    changes task frequency

    Paramaters:
        task :: the task key in cubesat.scheduled_tasks dict
    
    Returns:
        None
    """
    pass

def configure_task(self, task, *kwargs):
    pass

def upload_to_sd(self, args):
    pass

def download_from_sd(self, args):
    pass

def sd_rm(self, file):
    pass

def pl_cmd_arm(self, *args):
    pass

def pl_cmd_photo(self):
    pass

def img_burst(self, args):
    pass

def pl_cmd(self, cmd, *args):
    pass

def simulate(self, *args):
    """
    TODO ignore this while i work out simualation kinks
    simulate command. 
    passed args are keys in the self.cubesat.sim.simulate dict
    they TOGGLE simulation
    """
    for arg in args:
        if arg in self.cubesat.sim.simulate:
            self.cubesat.sim.simulate[arg] = not self.cubesat.sim.simulate[arg]
            write("Simulation for value: {} set  to {}" .format(arg, str(self.cubesat.sim.simulate[arg])))

########### helper functions for using usb_cdc.data ###########

def write(msg):
    """
    writes a string to usb_cdc.data
    appends \r\n
    """
    msg = msg + '\r\n'
    usb_cdc.data.write(bytes(msg, 'utf-8'))

def waitforinput():
    """
    waits for ANY input then throws the data away
    useful for pib verification
    """
    write("Press enter to continue")
    waitflag = True
    while waitflag:
        if usb_cdc.data.in_waiting:
            rx = usb_cdc.data.readline()
            if rx:
                waitflag = False
        time.sleep(1)