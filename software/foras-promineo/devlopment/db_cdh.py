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
    write('query: {}'.format(args))
    write(str(eval(args)))

def exec_cmd(self,args):
    arg = args[0]
    write('exec: {}'.format(arg))
    try:
        exec(bytes(arg, 'utf-8'))
    except Exception as e:
        write('Execution failed... : {}'.format(e))

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
    pass

def i2c_scan(self):
    while not self.cubesat.i2c1.try_lock():
        pass
    try:
        while True:
            print(
                "I2C addresses found:",
                [hex(device_address) for device_address in self.cubesat.i2c1.scan()],
            )
            time.sleep(2)
    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
       self.cubesat.i2c1.unlock()

def pib_verify(self):
    """
    PIB checkout function to verify functionality on the PIB
    """
    # verify imu
    write("verifing imu ....")
    write("Gyro 0 :"+str(self.cubesat.pib.imu.gyro0_r_raw))
    write("Gyro 1 :"+str(self.cubesat.pib.imu.gyro1_r_raw))
    write("Mag 0 :"+str(self.cubesat.pib.imu.mag0_r_raw))
    write("Mag 1 :"+str(self.cubesat.pib.imu.mag1_r_raw))
    write("Accel 0 :"+str(self.cubesat.pib.imu.accel0_r_raw))
    write("Accel 1 :"+str(self.cubesat.pib.imu.accel1_r_raw))
    write("")

    # verify io exp
    write("verifying io_exp")
    self.cubesat.pib.n_dac_lat0 = False
    time.sleep(1)
    self.cubesat.pib.n_dac_lat0 = True
    write("")

    # verify dac
    write("verifying dac")
    write("setting all outputs to 1.25V")
    self.cubesat.pib.dac.dac0 = 2^6
    self.cubesat.pib.dac.dac1 = 2^6
    self.cubesat.pib.dac.dac2 = 2^6
    write("sleeping 5s")
    write("")
    time.sleep(5)

    # verify amp
    write("verifing amp")
    write("turning all outputs ON")
    self.cubesat.pib.n_amp_shdn_xy = True
    self.cubesat.pib.n_amp_shdn_z = True
    write("sleeping 5s")
    write("")
    time.sleep(5)

    # verify h-bridge
    write("verifing h-bridge")
    write("turning all outputs ON in + direction")
    self.cubesat.pib.drv_ph_x = True
    self.cubesat.pib.drv_ph_y = True
    self.cubesat.pib.drv_ph_z = True
    self.cubesat.pib.drv_en_x = True
    self.cubesat.pib.drv_en_y = True
    self.cubesat.pib.drv_en_z = True
    self.cubesat.pib.n_drv_slp_x = True
    self.cubesat.pib.n_drv_slp_y = True
    self.cubesat.pib.n_drv_slp_z = True
    write("sleeping 5s")
    write("")
    time.sleep(5)

    # verify i sen
    write("verifing h-bridge")
    write("sense resistor is not installed, so readings should be around 1.25V")
    self.cubesat.pib.ch0_en = True
    refresh = self.cubesat.pib.adc.read
    write("CH0: "+str(self.cubesat.pib.adc.read))
    self.cubesat.pib.ch0_en = False
    refresh = self.cubesat.pib.adc.read
    self.cubesat.pib.ch1_en = True
    refresh = self.cubesat.pib.adc.read
    write("CH1: "+str(self.cubesat.pib.adc.read))
    self.cubesat.pib.ch1_en = False
    refresh = self.cubesat.pib.adc.read
    self.cubesat.pib.ch2_en = True
    refresh = self.cubesat.pib.adc.read
    write("CH2: "+str(self.cubesat.pib.adc.read))
    self.cubesat.pib.ch2_en = False
    write("sleeping 5s")
    write("")
    time.sleep(5)
       
    # verify rockblock
    write("rockblock verification not written")

    write("")
    write("returning things to idle")
    self.cubesat.pib.dac.dac0 = 0
    self.cubesat.pib.dac.dac1 = 0
    self.cubesat.pib.dac.dac2 = 0
    self.cubesat.pib.n_amp_shdn_xy = False
    self.cubesat.pib.n_amp_shdn_z = False
    self.cubesat.pib.drv_ph_x = False
    self.cubesat.pib.drv_ph_y = False
    self.cubesat.pib.drv_ph_z = False
    self.cubesat.pib.drv_en_x = False
    self.cubesat.pib.drv_en_y = False
    self.cubesat.pib.drv_en_z = False
    self.cubesat.pib.n_drv_slp_x = False
    self.cubesat.pib.n_drv_slp_y = False
    self.cubesat.pib.n_drv_slp_z = False
    write(" PIB checkout END")
    pass

########### helper functions for using usb_cdc.data ###########

#writes a string to usb_cdc.data
# appends \r\n 
def write(msg):
    msg = msg + '\r\n'
    usb_cdc.data.write(bytes(msg, 'utf-8'))
