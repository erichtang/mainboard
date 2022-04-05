"""
CircuitPython driver for PyCubed satellite board.
PyCubed Hardware Version: mainboard-v5-SLI
CircuitPython Version: 7.0.0 alpha
Library Repo: 

* Author(s): Max Holliday,
Fork'd by Marek Brodke, C. Hillis

To-Do
    1. Get IMU up and running, in this lib and it's own lib
    2. move template_task.debug to a lib so it can be used here too (ONLY FOR INIT)
    3. Invesitage purpose/use of merek's code for SD
    4. have proper things print to debug and log files
    5. 

"""

# Common CircuitPython Libs
#from syslog import LOG_DAEMON -- look into this
import board, microcontroller
import busio, time, sys
from storage import mount,umount,VfsFat
from analogio import AnalogIn
import digitalio, sdcardio, pwmio, tasko#, supervisor #marek added supervisor?

# Hardware Specific Libs
import pycubed_rfm9x # Radio
import neopixel # RGB LED
import bq25883 # USB Charger
import adm1176 # Power Monitor
import sli_imu # SLI added IMU lib, abstracted due to it also being on the PIB.
import adafruit_gps #need to play with gps reading procedure. 
#from mt_driver import mt_driver, mt_driver_simulated # magneto tourquer driver $$ this is completely different now
#from smart_buffer import smart_buffer # the buffer protocol -- commented out for now

# Common CircuitPython Libs
from os import listdir, stat, statvfs, mkdir, chdir
from os import remove, rmdir, getcwd #marek added
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

SEND_BUFF=bytearray(252) # marek removed this?

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
        
        self.vlowbatt=6.0 #adjust this value--------------------------------------------------------------------------------------------------------------------------------------
        self.send_buff = memoryview(SEND_BUFF)
        self.debug=True # set to false for flight?

        """
        # I think this needs to be moved down lower in the init -- looking into this, also pycubed has commands already implemented, IDK why marek tried to implement his own. looking into this
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
        """

        self.micro=microcontroller

        # table that stores whether or not a device is active or not
        self.hardware = {
                        'IMU':    False, #edit this one, maybe have each IMU device be it's own bool? i.e.
                        #'IMUx': {
                        #   'Gyro1' : False, ......}
                        # but that would make this table a-lot messier. maybe have it be -false on signle device failure, and deal w/ this being false regardless?
                        'Radio1': False,
                        'Radio2': False,
                        'SDcard': False,
                        'GPS':    False,
                        'WDT':    False,
                        'USB':    False,
                        'PWR':    False,
                        'MTDRIVERS': False,# marek added
                        'CAMERA': False} #marek added, rename to payload?

        # Define burn wires:
        self._relayA = digitalio.DigitalInOut(board.RELAY_A)
        self._relayA.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
        self._resetReg = digitalio.DigitalInOut(board.VBUS_RST)
        self._resetReg.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
        

        # Define battery voltage
        self._vbatt = AnalogIn(board.BATTERY)
        """ LOOK into this CH 
        # Define MPPT charge current measurement --- add current sense line to mainboard to read this effectively------------------------------------------- next mainboard REV
        self._ichrg = AnalogIn(board.L1PROG)
        self._chrg = digitalio.DigitalInOut(board.CHRG)
        self._chrg.switch_to_input()
        """

        # Define SPI,I2C,UART
        # for devices on the board, IMU, mt drivers etc,
        self.i2c1  = busio.I2C(board.SCL,board.SDA)
        self.spi  = board.SPI()
        self.uart1 = busio.UART(board.TX,board.RX)
        self.uart2 = busio.UART(board.TX2,board.RX2)
        self.uart3 = busio.UART(board.TX3,board.RX3)
        self.uart4 = busio.UART(board.TX4,board.RX4)

        # Define filesystem stuff
        self.logfile="/log.txt"

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

        # Initialize SD card (always init SD before anything else on spi bus)
        try:
            # Baud rate depends on the card, 4MHz should be safe
            _sd = sdcardio.SDCard(self.spi, board.SD_CS, baudrate=4000000)
            _vfs = VfsFat(_sd)
            mount(_vfs, "/sd")
            self.fs=_vfs
            sys.path.append("/sd")
            self.hardware['SDcard'] = True
            self.logfile="/sd/log.txt"
            """
            # ------------------------------------------ Start Section v

            # setting the directory where all generated data is stored
            self.storage_directory = "/sd/"

            # setting the system log file
            self.logfile = self.storage_directory + "log.txt"

            #setting the user's file name /sd/user_file_name
            #self.user_file_name = self.storage_directory + self.user_file_name

            # creating a big_buffer that the satellite can use for large file transfers
            #self.buffer = smart_buffer(self.storage_directory + "buf")

            # ------------------------------------------ End Section ^
            """
            self.log('[INIT][SD]')
        except Exception as e:
            self.log('[ERROR][SD Card]',e)
        
        # so you can tell the difference between boots in the log file
        self.log("----BOOT----")

        """
        # initializing connection to the camera
        try:
            self.cam_port = busio.UART(board.SDA2, board.SCL2, timeout=0.05, baudrate=115200)

        except Exception as e:
            self.log('[ERROR][CONNECTION_TO_CAMERA]',e)
        """
        
        # Initialize Neopixel
        try:
            self.neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
            self.neopixel[0] = (0,0,0)
            self.hardware['Neopixel'] = True
            self.log('[INIT][Neopixel]')
        except Exception as e:
            self.log('[WARNING][Neopixel]' + str(e))

        # Initialize USB charger
        try:
            self.usb = bq25883.BQ25883(self.i2c1)
            self.usb.charging = False
            self.usb.wdt = False
            self.usb.led=False
            self.usb.charging_current=8 #400mA
            self.usb_charging=False
            self.hardware['USB'] = True
            self.log('[INIT][USB Charger]')
        except Exception as e:
            self.log('[ERROR][USB Charger]'+ str(e))

        # Initialize Power Monitor
        try:
            self.pwr = adm1176.ADM1176(self.i2c1)
            self.pwr.sense_resistor = 1
            self.hardware['PWR'] = True
            self.log('[INIT][Power Monitor]')
        except Exception as e:
            self.log('[ERROR][Power Monitor]' + str(e))

        # Initialize IMU
        # Edit this for SLI imu changes, this will just error out every time.
        try:
            self.imu = sli_imu.IMU(self.i2c1, self.log)
            self.hardware['IMU'] = True
            self.log('[INIT][IMU]')
        except Exception as e:
            self.log('[ERROR][IMU]' + str(e))

        # Initialize GPS
        try:
            self.gps = adafruit_gps.GPS(self.uart1,debug=self.debug) # still powered off! #needs to be turned on somewhere else? -CH
            self.gps.timeout_handler=self.timeout_handler
            self.hardware['GPS'] = True
            self.log('[INIT][GPS]')
        except Exception as e:
            self.log('[ERROR][GPS]' + str(e))

        # Initialize radio #1 - UHF
        # Edit this for our mission spec. CH
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
            self.log('[INIT][Radio 1 - LoRa]')
        except Exception as e:
            self.log('[ERROR][Radio 1 - LoRa]' + str(e))

        # set PyCubed power mode
        self.power_mode = 'normal'

    def reinit(self,dev):
        dev=dev.lower()
        if   dev=='gps':
            self.gps.__init__(self.uart,debug=self.debug)
        elif dev=='pwr':
            self.pwr.__init__(self.i2c1)
        elif dev=='usb':
            self.usb.__init__(self.i2c1)
        elif dev=='imu':
            self.IMU.__init__(self.i2c1)
        else:
            self.log('Invalid Device? ->' + str(dev))
    """ look into fixing this. CH
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
    """
    @property
    def RGB(self):
        return self.neopixel[0]

    @RGB.setter
    def RGB(self,value):
        if self.hardware['Neopixel']:
            try:
                self.neopixel[0] = value
            except Exception as e:
                self.log('[WARNING]' + str(e))

    @property
    def charge_batteries(self):
        if self.hardware['USB']:
            self.log('[USB Charging][f{}]'.format(self.usb_charging))
            return self.usb_charging
    @charge_batteries.setter
    def charge_batteries(self,value):
        if self.hardware['USB']:
            self.usb_charging=value
            self.usb.led=value
            self.usb.charging=value

    @property
    def battery_voltage(self):
        #if not self.simulation: figure out what marek simulated
            _vbat=0
            for _ in range(50):
                _vbat+=self._vbatt.value * 3.3 / 65536
            _voltage = (_vbat/50)*(316+110)/110 # 316/110 voltage divider
            return _voltage # volts
        #else:
            #self.query_for_simulation("battery_voltage")

    @property
    def system_voltage(self):
        if self.hardware['PWR']:
            try:
                return self.pwr.read()[0] # volts
            except Exception as e:
                self.log('[WARNING][PWR Monitor]' + str(e))
        else:
            self.log('[WARNING][Power monitor not initialized]')

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

    """  FIX this CH -- need to add charge current measurement on MB
    def charge_current(self):
        
        LTC4121 solar charging IC with charge current monitoring
        See Programming the Charge Current section
        
        _charge = 0
        if self.solar_charging:
            _charge = self._ichrg.value * 3.3 / 65536
            _charge = ((_charge*988)/3010)*1000
        return _charge # mA
    
    @property
    def solar_charging(self):
        return not self._chrg.value
    """
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

    # writes a message to the log file
    # also prints it thru USB, can comment that line out if desired
    def log(self, msg):
        if self.hardware['SDcard']:
            with open(self.logfile, "a+") as f:
                t=int(time.monotonic())
                f.write('{}, {}\n'.format(t,msg))
        if self.debug:print(msg)

    def print_file(self,filedir=None,binary=False):
        if filedir==None:
            return
        self.log('\n--- Printing File: {} ---'.format(filedir))
        if binary:
            with open(filedir, "rb") as file:
                print(file.read())
                print('')
        else:
            with open(filedir, "r") as file:
                for line in file:
                    print(line.strip())

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
        needs edited. CH
        """
        self.log('[POWERMODE][f{}]'.format(mode))
        if 'min' in mode:
            self.RGB = (0,0,0)
            self.neopixel.brightness=0
            if self.hardware['Radio1']:
                self.radio1.sleep()
            if self.hardware['Radio2']:
                self.radio2.sleep()
            self.enable_rf.value = False
            if self.hardware['IMU']:
                self.IMU.gyro_powermode  = 0x14 # suspend mode
                self.IMU.accel_powermode = 0x10 # suspend mode
                self.IMU.mag_powermode   = 0x18 # suspend mode
            if self.hardware['PWR']:
                self.pwr.config('V_ONCE,I_ONCE')
            if self.hardware['GPS']:
                self.en_gps.value = False
            self.power_mode = 'minimum'

        elif 'norm' in mode:
            self.enable_rf.value = True
            if self.hardware['IMU']:
                self.reinit('IMU')
            if self.hardware['PWR']:
                self.pwr.config('V_CONT,I_CONT')
            if self.hardware['GPS']:
                self.en_gps.value = True
            self.power_mode = 'normal'
            # don't forget to reconfigure radios, gps, etc...
    """
    def new_file(self,substring,binary=False):
        '''
        substring something like '/data/DATA_'
        directory is created on the SD!
        int padded with zeros will be appended to the last found file
        '''
        if self.hardware['SDcard']:
            ff=''
            n=0
    """
    """ Figure out what is going on here
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

"""

    # ------------------------------------------ End Section
    """
    def burn(self,burn_num,dutycycle=0,freq=1000,duration=1):
        '''
        Operate burn wire circuits. Wont do anything unless the a nichrome burn wire
        has been installed.

        IMPORTANT: See "Burn Wire Info & Usage" of https://pycubed.org/resources
        before attempting to use this function!

        burn_num:  (string) which burn wire circuit to operate, must be either '1' or '2'
        dutycycle: (float) duty cycle percent, must be 0.0 to 100
        freq:      (float) frequency in Hz of the PWM pulse, default is 1000 Hz
        duration:  (float) duration in seconds the burn wire should be on
        '''
        # convert duty cycle % into 16-bit fractional up time
        dtycycl=int((dutycycle/100)*(0xFFFF))
        print('----- BURN WIRE CONFIGURATION -----')
        print('\tFrequency of: {}Hz\n\tDuty cycle of: {}% (int:{})\n\tDuration of {}sec'.format(freq,(100*dtycycl/0xFFFF) + ' ' + str(dtycycl) + ' ' + duration))
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
    """

    # ------------------------------------------ Start Section modified by Marek Brodke on 12/8/2021
    """
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
    """

cubesat = Satellite()
