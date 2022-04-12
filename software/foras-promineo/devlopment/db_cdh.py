import time
import usb_cdc

commands = {
    b'no-op': 'no-op',
}

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