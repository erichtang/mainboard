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
    write(eval(bytes(args,'utf-8')))

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
    write("Gyro 0 : {}".format(self.cubesat.pib.imu.gyro0))
    write("Gyro 1 : {}".format(self.cubesat.pib.imu.gyro1))
    write("Mag 0 : {}".format(self.cubesat.pib.imu.mag0))
    write("Mag 1 : {}".format(self.cubesat.pib.imu.mag1))
    write("Accel 0 : {}".format(self.cubesat.pib.imu.accel0))
    write("Accel 1 : {}".format(self.cubesat.pib.imu.accel1))
    write("")


    # verify io exp
    write("verifying io_exp... turning all outputs HIGH except SLP lines")
    self.cubesat.pib.n_dac_lat0 = True
    self.cubesat.pib.n_dac_lat0 = True
    self.cubesat.pib.n_amp_shdn_xy = False
    self.cubesat.pib.n_amp_shdn_z = False
    self.cubesat.pib.drv_ph_x = True
    self.cubesat.pib.drv_en_x = True
    self.cubesat.pib.n_drv_slp_x = False
    self.cubesat.pib.drv_ph_y = True
    self.cubesat.pib.drv_en_y = True
    self.cubesat.pib.n_drv_slp_y = False
    self.cubesat.pib.drv_ph_z = True
    self.cubesat.pib.drv_en_z = True
    self.cubesat.pib.n_drv_slp_z = False
    self.cubesat.pib.n_dac_rst = True
    write("")
    waitforinput()

    # verify dac
    write("verifying dac")
    write("setting all outputs to 1.25V")
    self.cubesat.pib.dac.dac0 = 2^6
    self.cubesat.pib.dac.dac1 = 2^6
    self.cubesat.pib.dac.dac2 = 2^6
    write("")
    waitforinput()

    # verify amp
    write("verifing amp")
    write("turning all outputs ON, output should be ~2.5V")
    self.cubesat.pib.n_amp_shdn_xy = True
    self.cubesat.pib.n_amp_shdn_z = True
    write("")
    waitforinput()

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
    write("")
    waitforinput()

    # verify i sen
    write("verifing sense line")
    write("sense resistor is not installed, so readings should be railed")
    self.cubesat.pib.adc.ch = 0
    write("CH0: {}".format(self.cubesat.pib.adc.read))
    time.sleep(0.01)
    write("CH0: {}".format(self.cubesat.pib.adc.read))
    self.cubesat.pib.adc.ch = 1
    write("CH1: {}".format(self.cubesat.pib.adc.read))
    time.sleep(0.01)
    write("CH1: {}".format(self.cubesat.pib.adc.read))
    self.cubesat.pib.adc.ch = 2
    write("CH2: {}".format(self.cubesat.pib.adc.read))
    time.sleep(0.01)
    write("CH2: {}".format(self.cubesat.pib.adc.read))
    self.cubesat.pib.adc.ch = 0
    write("")
    waitforinput()
       
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
    write("")

def simulate(self, *args):
    """
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