"""
CircuitPython driver for PyCubed satellite board.
PyCubed Hardware Version: mainboard-v05
CircuitPython Version: 7.0.0 alpha
Library Repo: https://github.com/pycubed/library_pycubed.py

* Author(s): Max Holliday, Marek Brodke

"""

# Common CircuitPython Libs
import board, microcontroller
import busio, time, sys
from storage import mount,umount,VfsFat
from analogio import AnalogIn
import digitalio, sdcardio, pwmio, tasko, supervisor

# Hardware Specific Libs
import pycubed_rfm9x # Radio
import bmx160 # IMU
import neopixel # RGB LED
import bq25883 # USB Charger
import adm1176 # Power Monitor
from mt_driver import mt_driver, mt_driver_simulated # magneto tourquer driver
from smart_buffer import smart_buffer # the buffer protocol

# Common CircuitPython Libs
from os import listdir, remove, stat, statvfs, mkdir, chdir, rmdir, getcwd
from bitflags import bitFlag,multiBitFlag,multiByte
from micropython import const

# NVM register numbers
_BOOTCNT  = const(0)
_VBUSRST  = const(6)
_STATECNT = const(7)
_TOUTS    = const(9)
_GSRSP    = const(10)
_ICHRG    = const(11)
_FLAG     = const(16)

class Satellite:           
    # General NVM counters
    c_boot      = multiBitFlag(register=_BOOTCNT,  lowest_bit=0, num_bits=8)
    c_vbusrst   = multiBitFlag(register=_VBUSRST,  lowest_bit=0, num_bits=8)
    c_state_err = multiBitFlag(register=_STATECNT, lowest_bit=0, num_bits=8)
    c_gs_resp   = multiBitFlag(register=_GSRSP,    lowest_bit=0, num_bits=8)
    c_ichrg     = multiBitFlag(register=_ICHRG,    lowest_bit=0, num_bits=8)

    # Define NVM flags
    f_lowbatt  = bitFlag(register=_FLAG, bit=0)
    f_solar    = bitFlag(register=_FLAG, bit=1)
    f_gpson    = bitFlag(register=_FLAG, bit=2)
    f_lowbtout = bitFlag(register=_FLAG, bit=3)
    f_gpsfix   = bitFlag(register=_FLAG, bit=4)
    f_shtdwn   = bitFlag(register=_FLAG, bit=5)

    def __init__(self):
        """
        Big init routine as the whole board is brought up.

        """
        self.BOOTTIME= const(time.time())
        self.data_cache={}
        self.filenumbers={}

        # the minimum voltage that the battery can have before the satellite enters low power mode
        self.vlowbatt=4.8

        # ------------------------------------------ Start Section v
       
        # something that I set that indicates how much time in minutes to wait until starting transmitting
        self.minutes_to_wait = 1

        # the name of the file where the user's uploaded code will be stored
        self.user_file_name = "user_file"

        # bool used to determine whether or not the user's file should be sent to the camera
        self.send_file_to_camera = False

        # password that every upload must begin with, must be 4 bytes currently
        self.password = b"MAIN"

        # all data sent to the ground must start with this
        self.start_communication = b"STAR"

        # file that things will be logged to
        self.logfile = "log.txt"

        # ends a communication
        self.end_communication = b"END_"

        # indicates if the game is running on the the camera
        self.game_is_running = False

        # if connected to the ground
        #if supervisor.runtime.serial_connected:
        #    self.connected = True
        #else:
        #    self.connected = False
        
        self.connected=False
        self.simulation=False

        # ------------------------------------------ End Section ^

        self.micro=microcontroller

        # ------------------------------------------ Start Section v

        # table that stores whether or not a device is active or not
        self.hardware = {
                        'IMU':    False,
                        'Radio1': False,
                        'Radio2': False,
                        'SDcard': False,
                        'GPS':    False,
                        'WDT':    False,
                        'USB':    False,
                        'PWR':    False,
                        'MTDRIVERS': False,
                        'CAMERA': False}

        # ------------------------------------------ End Section ^

        # Define burn wires:
        self._relayA = digitalio.DigitalInOut(board.RELAY_A)
        self._relayA.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
        self._resetReg = digitalio.DigitalInOut(board.VBUS_RST)
        self._resetReg.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)

        # Define battery voltage
        self._vbatt = AnalogIn(board.BATTERY)

        # Define MPPT charge current measurement
        ################################################# look at this with revised solar charger CH 12/14
        self._ichrg = AnalogIn(board.L1PROG)
        self._chrg = digitalio.DigitalInOut(board.CHRG)
        self._chrg.switch_to_input()

        # Define SPI,I2C,UART
        # for devices on the board, IMU, mt drivers etc,
        self.i2c1  = busio.I2C(board.SCL,board.SDA)

        # connection to radios
        self.spi  = board.SPI()

        # gps connection
        self.uart = busio.UART(board.TX,board.RX)

        # Initialize SD card (always init SD before anything else on spi bus)
        try:
            # Baud rate depends on the card, 4MHz should be safe
            _sd = sdcardio.SDCard(self.spi, board.SD_CS, baudrate=4000000)
            _vfs = VfsFat(_sd)
            # mounting the sd to the virtual file system
            mount(_vfs, "/sd")
            self.fs=_vfs
            
            # adding the path to the visible directory tree
            sys.path.append("/sd")
            
            # setting the SDcard row of the hardware table to true
            self.hardware['SDcard'] = True

            # ------------------------------------------ Start Section v

            # setting the directory where all generated data is stored
            self.storage_directory = "/sd/"

            # setting the system log file
            self.logfile = self.storage_directory + "log.txt"

            #setting the user's file name /sd/user_file_name
            self.user_file_name = self.storage_directory + self.user_file_name

            # creating a big_buffer that the satellite can use for large file transfers
            self.buffer = smart_buffer(self.storage_directory + "buf")

            # ------------------------------------------ End Section ^
        except Exception as e:
            self.log('[ERROR][SD Card]:' + str(e))

        # so you can tell the difference between boots in the log file
        self.log("----BOOT----")
        # ------------------------------------------ Start Section v

        # initializing connection to the camera
        try:
            self.cam_port = busio.UART(board.SDA2, board.SCL2, timeout=0.05, baudrate=115200)

        except Exception as e:
            self.log('[ERROR][CONNECTION_TO_CAMERA]',e)

        # ------------------------------------------ End Section ^

        # Define GPS
        self.en_gps = digitalio.DigitalInOut(board.EN_GPS)
        self.en_gps.switch_to_output()

        # Define radio
        _rf_cs1 = digitalio.DigitalInOut(board.RF1_CS)
        _rf_rst1 = digitalio.DigitalInOut(board.RF1_RST)
        self.enable_rf = digitalio.DigitalInOut(board.EN_RF)
        self.radio1_DIO0=digitalio.DigitalInOut(board.RF1_IO0)
        # self.enable_rf.switch_to_output(value=False) # if U21
        self.enable_rf.switch_to_output(value=True) # if U7
        _rf_cs1.switch_to_output(value=True)
        _rf_rst1.switch_to_output(value=True)
        self.radio1_DIO0.switch_to_input()

        # ------------------------------------------ Start Section v

        # initializing magneto torquer driver board connection 
        try:
            # initializing the driver board at the address 0x58 on the i2c bus
            if not self.simulation:
                pass
                #self.driver_x = mt_driver(0x58, self.i2c1)
                #self.driver_y = mt_driver(0x59, self.i2c1)
                #self.driver_z = mt_driver(0x60, self.i2c1)
            else:
                self.driver_x = mt_driver_simulated(0x58, self.send_result_of_simulation)
                self.driver_y = mt_driver_simulated(0x59, self.send_result_of_simulation)
                self.driver_z = mt_driver_simulated(0x60, self.send_result_of_simulation)

            self.hardware['MTDRIVERS'] = True
        
        except Exception as e:
            self.error_encountered = True
            self.log('[WARNING][MT_DRIVER]:' + str(e))

        # ------------------------------------------ End Section ^

        # Initialize Neopixel
        try:
            self.neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
            self.neopixel[0] = (0,0,0)
            self.hardware['Neopixel'] = True
        except Exception as e:
            self.error_encountered = True
            self.log('[WARNING][Neopixel]:' + str(e))

        # Initialize USB charger
        try:
            self.usb = bq25883.BQ25883(self.i2c1)
            self.usb.charging = False
            self.usb.wdt = False
            self.usb.led=False
            self.usb.charging_current=8 #400mA
            self.usb_charging=False
            self.hardware['USB'] = True
        except Exception as e:
            self.error_encountered = True
            self.log('[ERROR][USB Charger]:' + str(e))

        # Initialize Power Monitor
        try:
            self.pwr = adm1176.ADM1176(self.i2c1)
            self.pwr.sense_resistor = 1
            self.hardware['PWR'] = True
        except Exception as e:
            self.error_encountered = True
            self.log('[ERROR][Power Monitor]:' + str(e))

        # Initialize IMU
        try:
            self.IMU = bmx160.BMX160_I2C(self.i2c1)
            self.hardware['IMU'] = True
        except Exception as e:
            self.error_encountered = True
            self.log('[ERROR][IMU]:' + str(e))

        # Initialize GPS
        """
        try:
            self.gps = GPS(self.uart,debug=False) # still powered off!
            self.gps.timeout_handler=self.timeout_handler
            self.hardware['GPS'] = True
        except Exception as e:
            if self.debug:
                self.log('[ERROR][GPS]:' + str(e))
        """

        # Initialize radio #1 - UHF
        try:
            self.radio1 = pycubed_rfm9x.RFM9x(self.spi, _rf_cs1, _rf_rst1,
                433.0,code_rate=8,baudrate=1320000)
            # Default LoRa Modulation Settings
            # Frequency: 433 MHz, SF7, BW125kHz, CR4/8, Preamble=8, CRC=True
            self.radio1.dio0=self.radio1_DIO0
            self.radio1.enable_crc=True
            self.radio1.ack_delay=0.2
            self.radio1.sleep()
            self.hardware['Radio1'] = True
        except Exception as e:
            self.error_encountered = True
            self.log('[ERROR][RADIO 1]:' + str(e))

        # set PyCubed power mode
        self.power_mode = 'normal'


    def reinit(self,dev):
        dev=dev.lower()
        if   dev=='gps':
            self.gps.__init__(self.uart,debug=False)
        elif dev=='pwr':
            self.pwr.__init__(self.i2c1)
        elif dev=='usb':
            self.usb.__init__(self.i2c1)
        elif dev=='imu':
            self.IMU.__init__(self.i2c1)
        else:
            self.log('Invalid Device? ->' + dev)

    @property
    def acceleration(self):
        if not self.simulation:
            if self.hardware['IMU']:
                return self.IMU.accel # m/s^2
        else:
            return self.query_for_simulation(b"acceleration")

    @property
    def magnetic(self):
        if not self.simulation:
            if self.hardware['IMU']:
                return self.IMU.mag # uT
        else:
            return self.query_for_simulation(b"magnetic")

    @property
    def gyro(self):
        if not self.simulation:
            if self.hardware['IMU']:
                return self.IMU.gyro # deg/s
        else:
            return self.query_for_simulation(b"gyro")

    @property
    def temperature(self):
        if not self.simulation:
            if self.hardware['IMU']:
                return self.IMU.temperature # Celsius
        else:
            return self.query_for_simulation(b"temperature")

    @property
    def RGB(self):
        return self.neopixel[0]

    @RGB.setter
    def RGB(self,value):
        if self.hardware['Neopixel']:
            try:
                self.neopixel[0] = value
            except Exception as e:
                self.log('[WARNING]:' + str(e))

    @property
    def charge_batteries(self):
        if self.hardware['USB']:
            return self.usb_charging

    @charge_batteries.setter
    def charge_batteries(self,value):
        if self.hardware['USB']:
            self.usb_charging=value
            self.usb.led=value
            self.usb.charging=value

    @property
    def battery_voltage(self):
        if not self.simulation:
            _vbat=0
            for _ in range(50):
                _vbat+=self._vbatt.value * 3.3 / 65536
            _voltage = (_vbat/50)*(316+110)/110 # 316/110 voltage divider

            return _voltage # volts
        else:
            self.query_for_simulation("battery_voltage")

    @property
    def system_voltage(self):
        if self.hardware['PWR']:
            try:
                return self.pwr.read()[0] # volts
            except Exception as e:
                self.log('[WARNING][PWR Monitor]:' + str(e))
        else:
            self.log('[WARNING] Power monitor not initialized')

    @property
    def current_draw(self):
        """
        current draw from batteries
        NOT accurate if powered via USB
        """
        if self.hardware['PWR']:
            idraw=0
            try:
                for _ in range(50): # average 50 readings
                    idraw+=self.pwr.read()[1]
                return (idraw/50)*1000 # mA
            except Exception as e:
                self.log('[WARNING][PWR Monitor]' + str(e))
        else:
            self.log('[WARNING] Power monitor not initialized')

    def charge_current(self):
        """
        LTC4121 solar charging IC with charge current monitoring
        See Programming the Charge Current section
        """
        _charge = 0
        if self.solar_charging:
            _charge = self._ichrg.value * 3.3 / 65536
            _charge = ((_charge*988)/3010)*1000
        return _charge # mA

    @property
    def solar_charging(self):
        return not self._chrg.value

    @property
    def reset_vbus(self):
        # unmount SD card to avoid errors
        if self.hardware['SDcard']:
            try:
                umount('/sd')
                self.spi.deinit()
                time.sleep(3)
            except Exception as e:
                self.log('vbus reset error?' + str(e))
                pass
        self._resetReg.drive_mode=digitalio.DriveMode.PUSH_PULL
        self._resetReg.value=1

    # ------------------------------------------ Start Section modified by Marek Brodke on 11/24/2021, 12/8/2021 v

    # writes a message to the log file
    def log(self, msg):
        if not self.connected: # if debugging usb is not connected
            with open(self.logfile, "a+") as f: # opening the log file for appending
                t=int(time.monotonic())
                f.write('{}, {}\n'.format(t,msg)) # appending the time and message to file

        else: # if debugging usb is connected
            print(msg)


    # ------------------------------------------ End Section ^

    def print_file(self,filedir=None,binary=False):
        if filedir==None:
            return
        self.log('\n--- Printing File: {} ---'.format(filedir))
        if binary:
            with open(filedir, "rb") as file:
                self.log(file.read())
                self.log('')
        else:
            with open(filedir, "r") as file:
                for line in file:
                    self.log(line.strip())


    def timeout_handler(self):
        self.log('Incrementing timeout register')
        if (self.micro.nvm[_TOUTS] + 1) >= 255:
            self.micro.nvm[_TOUTS]=0
            # soft reset
            self.micro.on_next_reset(self.micro.RunMode.NORMAL)
            self.micro.reset()
        else:
            self.micro.nvm[_TOUTS] += 1


    def powermode(self,mode):
        """
        Configure the hardware for minimum or normal power consumption
        Add custom modes for mission-specific control
        """
        if 'min' in mode:
            # turning of the neopixel
            self.RGB = (0,0,0)
            self.neopixel.brightness=0

            # putting the LoRa radio to sleep
            if self.hardware['Radio1']:
                self.radio1.sleep()
            
            # other slot on the main board for a radio
            #if self.hardware['Radio2']:
            #    self.radio2.sleep()
            self.enable_rf.value = False
            
            # putting the IMU to sleep
            if self.hardware['IMU']:
                self.IMU.gyro_powermode  = 0x14 # suspend mode
                self.IMU.accel_powermode = 0x10 # suspend mode
                self.IMU.mag_powermode   = 0x18 # suspend mode
            
            # putting the power moniter to sleep
            if self.hardware['PWR']:
                self.pwr.config('V_ONCE,I_ONCE')
            
            # putting the gps to sleep
            if self.hardware['GPS']:
                self.en_gps.value = False
            
            # setting the flag that indicates the power mode of the satellite
            self.power_mode = 'minimum'

        # normal power mode
        elif 'norm' in mode:
            
            self.enable_rf.value = True
            
            # reinitializing IMU
            if self.hardware['IMU']:
                self.reinit('IMU')
            
            # reinitializing power monitor
            if self.hardware['PWR']:
                self.pwr.config('V_CONT,I_CONT')
            
            # reinitializing gps
            if self.hardware['GPS']:
                self.en_gps.value = True
            
             # setting the flag that indicates the power mode of the satellite
            self.power_mode = 'normal'
            # don't forget to reconfigure radios, gps, etc...

    # ------------------------------------------ Start Section

    # removes a file with the inputted path or name
    def remove_file(self, file_name):
        # if the sd card is inserted
        if self.hardware['SDcard']:
            _pwd = getcwd()

            # removing / at the front if there is one
            if file_name[0] == '/':
                file_name = file_name[1:]

            # extracting the path and file name from the inputted
            _folder=file_name[:file_name.rfind('/')+1]
            _file=file_name[file_name.rfind('/')+1:]

            try:
                # going to the path specified in the inputted file name
                chdir(self.storage_directory + _folder)
            except OSError:
                # if here the path does not exist so show error message and exit function
                self.log("ERROR: INVALID PATH" + _folder)
                return
            
            try:
                # removes the file
                remove(_file)
            except Exception as e:
                # catches errors like if the file does not exist
                self.log("ERROR:" + str(e))
            
            # going back to root directory 
            chdir(_pwd)

        else:
            # sd card is not insert so show it
            self.log("ERROR: SD NOT FOUND")


    # creates a new file with a path and name equal to the one inputted
    # if the path does not exist it is created
    def new_file(self,substring):
        # if the sd card is inserted
        if self.hardware['SDcard']:
            _pwd = getcwd()
            # removing / at the front if there is one
            if substring[0] == '/':
                substring = substring[1:]

            # extracting the path and file name from the inputted
            _folder=substring[:substring.rfind('/')+1]
            _file=substring[substring.rfind('/')+1:]

            # going to the path specified in the inputted file name
            try: chdir(self.storage_directory + _folder)
            except OSError:
                # if here the path does not exist so it makes it
                try: mkdir(self.storage_directory + _folder)
                except Exception as e:
                    # should not be here but catches any problems
                    self.log("ERROR:" + str(e))
        
            try:
                # creates the file
                f = open(_file, 'w')
                f.close()

            except Exception as e:
                self.log("ERROR:" + str(e))

            # going back to root directory
            chdir(_pwd)
           
        else:
            # sd card is not insert so show it
            self.log("ERROR: SD NOT FOUND")


    # creates a new directory with a path and name equal to the one inputted
    # if the path does not exist it is created
    def new_directory(self, substring):
        # if the sd card is inserted
        if self.hardware['SDcard']:
            # removing / at the front if there is one
            if substring[0] == '/':
                substring = substring[1:]
            
            # if here the path does not exist so it makes it
            try: mkdir(self.storage_directory + substring)
            except Exception as e:
                # should not be here but catches any problems
                self.log("ERROR:" + str(e))

           
        else:
            # sd card is not insert so show it
            self.log("ERROR: SD NOT FOUND")


    # removes a directory with a path and name equal to the one inputted
    # if the path does not exist nothing is done
    def remove_directory(self, substring):
        # if the sd card is inserted
        if self.hardware['SDcard']:
            # removing / at the front if there is one
            if substring[0] == '/':
                substring = substring[1:]
            
            # if here the path does not exist so it makes it
            try: rmdir(self.storage_directory + substring)
            except Exception as e:
                # should not be here but catches any problems
                self.log("ERROR:" + str(e))
                    
           
        else:
            # sd card is not insert so show it
            self.log("ERROR: SD NOT FOUND")


    # ------------------------------------------ End Section
    '''
    def burn(self,burn_num,dutycycle=0,freq=1000,duration=1):
        """
        Operate burn wire circuits. Wont do anything unless the a nichrome burn wire
        has been installed.

        IMPORTANT: See "Burn Wire Info & Usage" of https://pycubed.org/resources
        before attempting to use this function!

        burn_num:  (string) which burn wire circuit to operate, must be either '1' or '2'
        dutycycle: (float) duty cycle percent, must be 0.0 to 100
        freq:      (float) frequency in Hz of the PWM pulse, default is 1000 Hz
        duration:  (float) duration in seconds the burn wire should be on
        """
        # convert duty cycle % into 16-bit fractional up time
        dtycycl=int((dutycycle/100)*(0xFFFF))
        self.log('----- BURN WIRE CONFIGURATION -----')
        self.log('\tFrequency of: {}Hz\n\tDuty cycle of: {}% (int:{})\n\tDuration of {}sec'.format(freq,(100*dtycycl/0xFFFF) + ' ' + str(dtycycl) + ' ' + duration))
        # create our PWM object for the respective pin
        # not active since duty_cycle is set to 0 (for now)
        if '1' in burn_num:
            burnwire = pwmio.PWMOut(board.BURN1, frequency=freq, duty_cycle=0)
        elif '2' in burn_num:
            burnwire = pwmio.PWMOut(board.BURN2, frequency=freq, duty_cycle=0)
        else:
            return False
        # Configure the relay control pin & open relay
        self._relayA.drive_mode=digitalio.DriveMode.PUSH_PULL
        self._relayA.value = 1
        self.RGB=(255,0,0)
        # Pause to ensure relay is open
        time.sleep(0.5)
        # Set the duty cycle over 0%
        # This starts the burn!
        burnwire.duty_cycle=dtycycl
        time.sleep(duration)
        # Clean up
        self._relayA.value = 0
        burnwire.duty_cycle=0
        self.RGB=(0,0,0)
        burnwire.deinit()
        self._relayA.drive_mode=digitalio.DriveMode.OPEN_DRAIN
        return True
    '''

    # ------------------------------------------ Start Section modified by Marek Brodke on 12/8/2021

    def query_for_simulation(self, which):
        '''
        Sends a query for information to the computer connected to this one. This function requires tight integration with the software
        on the connected computer.

        :param which: what value to ask for from the connected computer

        :return: the data sent from the connected computer
        '''
        self.send_to_ground(b"GET_" + which)
        return eval(input())


    def send_result_of_simulation(self, device, result):
        '''
        Sends the device name and the value that it would have been set to

        :param device: the name of the device that the value was sent to, can be anything as long it can be converted to a string
        :param result: the value sent the device with the inputted name
        
        :return: None
        '''
        self.send_to_ground("SET_{}{}".format(str(device), str(result)).encode("utf-8", 'w'))


    def send_buffer_to_camera(self, clear_after=True):
        '''
        sends the data in the buffer to the camera

        :param clear_after: (boolean) if you want to clear the buffer after it is sent, default value is True

        :return: None
        '''
        # sends the password to the camera
        self.cam_port.write(self.password)
        
        # writes the data in the buffer to the camera port, clears it after if specified
        self.buffer.write_to_target(target=self.cam_port, clear_after_write=clear_after)
        
        # sends the end communication bytes to the camera
        self.cam_port.write(self.end_communication)


    def send_to_ground(self, value):
        '''
        sends the inputted value to the ground with the start and end bytes

        :param value: a bytes or bytearray object that holds the data that you want to send to the ground
        
        :return: None
        '''

        # if the input is a bytes or bytearray object
        if isinstance(value, (bytes, bytearray)): 
            # sending the start bytes
            sys.stdout.write(self.start_communication)
            
            # sending the inputted data
            sys.stdout.write(value)

            # sending the end bytes
            sys.stdout.write(self.end_communication)
        
        # sending an error message to the ground
        else: sys.stdout.write(self.start_communication + b"Invalid type to send" + self.end_communication)


    def send_buffer_to_ground(self, clear_after=True):
        '''
        Sends the data that is present in the buffer to the ground

        :param clear_after: (boolean) if you want to clear the buffer after it is sent, default value is True
        
        :return: None
        '''
        # temporary implementation until radios are figured out
        sys.stdout.write(self.start_communication)
        for i in range(0, len(self.buffer)):
            sys.stdout.write(self.buffer.get(i, 1))
        #self.buffer.write_to_target(target=sys.stdout, clear_after_write=clear_after)
        sys.stdout.write(self.end_communication)


    def get_camera_into_buffer(self, timeout=None, clear_buffer_before=True):
        '''
        reads data that is sent from the camera into the buffer

        :param timeout: (float) time in seconds to change the timeout of the port to, can be a decimal
        :param clear_buffer: (boolean) if you want to empty the buffer before data is added to it
        
        :return: None

        '''
        if clear_buffer_before: self.buffer.clear()
        if timeout is not None: # if the timeout of the port was overriden by an argument
            original_timeout = self.cam_port.timeout # recording the original so it can be overridden
            self.cam_port.timeout = timeout # setting the timeout of the port to the inputted value

        # reads from the camera into the buffer
        #self.buffer.read_from_target(self.cam_port, append=not(clear_buffer_before), start_condition=self.password, stop_condition=self.end_communication)

        
        return_val = b""

        # makes sure that the correct number of bytes are read, for this algorithm to work
        while len(return_val) < len(self.password):
            data = self.cam_port.read(1) # reading from the port
            if data is None:
                return False# if port timeout, bad, returns nothing
            return_val += data

        if return_val != self.password: return

        self.send_to_ground(b"got password from camera")
        while True:
            data = self.cam_port.read(1) # reading a byte from the target
            # if no data was returned, bad, exits loop
            if data is None: break
            #return_val = return_val[1:] + data

            # if recieved the end communication, exits the loop
            #if return_val == self.end_communication: break
            
            # adding data to the Buffer
            self.buffer.append(data)

        print(len(self.buffer))

        self.send_to_ground(b"got the end from the camera")

        if timeout is not None: self.cam_port.timeout = original_timeout # if the value was overridden it is changed back to what it was

        #return return_val[len(self.password) : -1 * len(self.end_communication)] # returns the recieved data with the end communication and password bytes removed


    def get_ground_into_buffer(self, clear_buffer_before=True):
        '''
        gets data transmitted from the ground, returns this in bytes form
        this I made this so that when a radio is used instead of the usb nothing changes besides this function

        :param clear_buffer: (boolean) if you want to empty the buffer before data is added to it

        :return: None

        '''
        # clears if the option was provided
        if clear_buffer_before: self.buffer.clear()
        
        # init
        data = None

        # if there are bytes available to this device
        if supervisor.runtime.serial_bytes_available:
            value = input() # reads the bytes
            # if the data starts with the password and ends with end communication
            if value.startswith(self.password.decode('utf-8')) and value.endswith(self.end_communication.decode('utf-8')):
                # removes the password and end communication bytes
                data = value[len(self.password.decode('utf-8')) : -1 * len(self.end_communication.decode('utf-8'))].encode('utf-8')
                
                # adds the data to the buffer
                self.buffer.append(data)

    # ------------------------------------------ End Section

# instantiation
cubesat = Satellite()

