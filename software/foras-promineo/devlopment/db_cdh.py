import time
import usb_cdc.data as db

commands = [
    'no-op',
    'hreset',
    'shutdown',
    'query',
    'exec_cmd',
]

########### commands without arguments ###########
def noop(self):
    db.write('no-op ACK')
    pass

def hreset(self):
    db.write('Resetting')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        db.write('Reset Failed')

########### commands with arguments ###########

def query(self,args):
    db.write('query: {}'.format(args))
    db.write(str(eval(args)))

def exec_cmd(self,args):
    db.write('exec: {}'.format(args))
    try:
        exec(args)
    except Exception as e:
        db.write('Execution failed... : {}'.format(e))

def get_imu_offset(write = False):
    # write offset detection here
    pass

def print_file (path):
    pass 