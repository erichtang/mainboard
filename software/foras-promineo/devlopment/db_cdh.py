import time
import usb_cdc
from debugcolor import co

########### commands without arguments ###########
def noop(self):
    write(co('ACK', 'green'))

def hreset(self):
    write('Resetting')
    try:
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        write('Reset Failed')

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

def get_imu_offset(self, args):
    """
    records RAW offset's of imu paramaters.
    write currently inimplemented (allowing automatic compensation of calculated offsets when it is)
    args[0] = x : # of measurements taken and averaged
    args[1] (default False) = wr : when True writes offsets to calibration dict. doesn't have to be passed.
    """
    #how to get offset with magnetometer?
    #add tabple entries for PIB
    polling_dict = {
        'gyro0': self.cubesat.imu.gyro0_r_raw,
        'gyro1': self.cubesat.imu.gyro1_r_raw,
        'mag0' : self.cubesat.imu.mag0_r_raw,
        'mag1' : self.cubesat.imu.mag1_r_raw,
        'accel0': self.cubesat.imu.accel0_r_raw,
        'accel1': self.cubesat.imu.accel1_r_raw,
    }
    #args extraction
    x = int(args[0])
    if len(args)==2:
        wr = args[1]
    else:
        wr = False
    #execution of function
    for device in polling_dict:
        #write(device)
        i = 0
        temp_avg = [0,0,0]
        while i < x :
            #get measurements
            temp = polling_dict[device]
            if temp is None:
                write("Device {} returned None on i = {} out of {}".format(device, i, x))
                temp_avg = None
                break
            else:
                for meas in range(len(temp_avg)):
                    temp_avg[meas] =+ temp[meas]
            time.sleep(0.01)
            i+=1
        #average
        if temp_avg is not None:
            for num in range(len(temp_avg)):
                temp_avg[num] = int(temp_avg[num]/x) #whole numbers, factional offsets would not make sense for a raw value.
            #print 
            write("Device {} Offset Calculation for {} readings: ".format(device, x) + co('{}'.format(temp_avg), 'green', 'bold'))

def print_file (path):
    pass 

def startstoptask(self, args):
    """
    starts or stops specified task.
    args[0] = task name
    args[1] = "st" or "sp"
    """

########### helper functions for using usb_cdc.data ###########

#writes a string to usb_cdc.data
# appends \r\n 
def write(msg):
    msg = msg + '\r\n'
    usb_cdc.data.write(bytes(msg, 'utf-8'))
