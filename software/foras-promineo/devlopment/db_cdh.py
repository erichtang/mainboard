import time
import usb_cdc

########### commands without arguments ###########
def noop(self):
    usb_cdc.data.write('no-op ACK')
    pass

def hreset(self):
    usb_cdc.data.write('Resetting')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        usb_cdc.data.write('Reset Failed')

########### commands with arguments ###########

def query(self,args):
    usb_cdc.data.write('query: {}'.format(args))
    usb_cdc.data.write(str(eval(args)))

def exec_cmd(self,args):
    usb_cdc.data.write('exec: {}'.format(args))
    try:
        exec(args)
    except Exception as e:
        usb_cdc.data.write('Execution failed... : {}'.format(e))

def get_imu_offset(write = False):
    # write offset detection here
    pass

def print_file (path):
    pass 

########### helper functions for using usb_cdc.data ###########

#writes a string to usb_cdc.data
def write(msg):
    usb_cdc.data.write(bytes(msg, 'utf-8'))

#reads a string of usb_cdc.data.readline
    #timeout for usb_cdc must be set, is currently set in usb_db_cdh.__init__
def read():
    msg = usb_cdc.data.readline()
    msg.decode('utf-8')
    msg.remove('\n', '\r') #do i need to scrub \n and \r?

#takes a string of comma separated args and extracts each string between , to a list
def args_extractor(args):
    pass
