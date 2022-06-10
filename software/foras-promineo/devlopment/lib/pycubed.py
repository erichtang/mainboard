"""
CircuitPython driver for PyCubed satellite board.
PyCubed Hardware Version: mainboard-v5-SLI
CircuitPython Version: 7.0.0 alpha
Library Repo: 

* Author(s): Max Holliday,
* Edited for Foras Promineo by : C. Hillis , M. Brodke
"""

# Common CircuitPython Libs
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
import foras_promineo_pib
import foras_promineo_payload
import simulation
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

SEND_BUFF=bytearray(252)

class Satellite:           
    # General NVM counters -- LOOK INTO THESE
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

    #Foras Promineo flags
    f_deployed = bitFlag(register=_FLAG, bit=6)

    def __init__(self):
        """
        Big init routine as the whole board is brought up.
        """
        # default config dict. will get updated if config.bak file exists
        self.cfg={
            'id':0xFA,  # default sat id
            'gs':0xAB,  # ground station id
            'st':5,     # sleep time exponent 1e5 sec
            'lb':6.0,   # low battery voltage (V)
        }
        self.BOOTTIME= const(time.time())
        self.data_cache={}
        self.filenumbers={}
        self.micro = microcontroller
        self.send_buff = memoryview(SEND_BUFF)
        self.debug=True       
        self.hardware = {
                        'IMU':     False,
                        'Radio1':  False,
                        'Radio2':  False,
                        'SDcard':  False,
                        'GPS':     False,
                        'WDT':     False,
                        'USB':     False,
                        'BUS_PWR': False,
                        'CHRG_PWR':False,
                        'PIB':     False,
                        'PAYLOAD': False,
                        } 

        # Define burn wires:
        self._relayA = digitalio.DigitalInOut(board.RELAY_A)
        self._relayA.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
        self._resetReg = digitalio.DigitalInOut(board.VBUS_RST)
        self._resetReg.switch_to_output(drive_mode=digitalio.DriveMode.OPEN_DRAIN)
        

        # Define battery voltage
        self._vbatt = AnalogIn(board.BATTERY)

        #define solar voltage
        #self._vsolar = AnalogIn(board...)

        # TODO LOOK into this CH 
        # Define MPPT charge current measurement --- add current sense line to mainboard to read this effectively------------------------------------------- next mainboard REV
        self._ichrg = 0 # TEMP UNTILL NEXT MAINBOARD IS RECIEVED
        self._chrg = digitalio.DigitalInOut(board.CHRG)
        self._chrg.switch_to_input()
        # not in firmware yet self._chrg_shdn = digitalio.DigitalInOut(board.PB21)
        #self._chrg_shdn.switch_to_output()
        
        # Define SPI,I2C,UART
        # TODO i2c_rst function needs modified to recover from an i2c lockup wihtout a soft reset. Will entail re-initing all i2c devices....
        self.i2c_rst() # sometimes during a soft reset i will get a lockup, this resets the i2c line and resets hangups
        self.i2c1 = busio.I2C(board.SCL,board.SDA,frequency=400000)
        self.spi  = board.SPI()
        self.uart1 = busio.UART(board.TX,board.RX) # radio1 UART
        self.uart2 = busio.UART(board.TX2,board.RX2, timeout=.1, baudrate=256000 ,recieve_buffer_size=240) # payload UART
        self.uart3 = busio.UART(board.TX3,board.RX3) # rockblock UART
        self.uart4 = busio.UART(board.TX4,board.RX4) # startracker UART

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
            self.log('[INIT][SD]')
        except Exception as e:
            self.log('[ERROR][INIT][SD Card]: {}'.format(e))
        
        print("----BOOT----")
        
        # Initialize Neopixel
        try:
            self.neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
            self.neopixel[0] = (0,0,0)
            self.hardware['Neopixel'] = True
            print('[INIT][Neopixel]')
        except Exception as e:
            print('[WARNING][Neopixel]: {}'.format(e))

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
            self.log('[ERROR][INIT][USB Charger]: {}'.format(e))

        # Initialize Power Monitor 1 -- current to bus
        try:
            self.bus_pwr = adm1176.ADM1176(self.i2c1)
            self.bus_pwr.sense_resistor = 1
            self.hardware['BUS_PWR'] = True 
            self.log('[INIT][Bus Power Monitor]')
        except Exception as e:
            self.log('[ERROR][INIT][Bus Power Monitor]: {}'.format(e))

        # Initialize Power Monitor 2 -- current to batt
        try:
            self.chrg_pwr = adm1176.ADM1176(self.i2c1, addr=0x90)  #update address
            self.chrg_pwr.sense_resistor = 1
            self.hardware['CHRG_PWR'] = True
            self.log('[INIT][CHRG Power Monitor]')
        except Exception as e:
            self.log('[ERROR][INIT][CHRG Power Monitor]: {}'.format(e))

        # Initialize IMU
        try:
            self.imu = sli_imu.IMU(self, 'IMU')
            self.hardware['IMU'] = True
            self.log('[INIT][IMU]')
        except Exception as e:
            self.log('[ERROR][INIT][IMU]: {}'.format(e))

        # Initialize GPS
        try:
            self.gps = adafruit_gps.GPS(self.uart1,debug=self.debug) # still powered off! #needs to be turned on somewhere else? -CH
            self.gps.timeout_handler=self.timeout_handler
            self.hardware['GPS'] = True
            self.log('[INIT][GPS]')
        except Exception as e:
            self.log('[ERROR][INIT][GPS]: {}'.format(e))

        # Initialize radio #1 - UHF
        # TODO Edit this for our mission spec. CH
        try:
            self.radio1 = pycubed_rfm9x.RFM9x(self.spi, _rf_cs1, _rf_rst1,
                433.0,code_rate=8,baudrate=1320000)
            # Default LoRa Modulation Settings
            # Frequency: 433 MHz, SF7, BW125kHz, CR4/8, Preamble=8, CRC=True
            self.radio1.dio0=self.radio1_DIO0
            self.radio1.enable_crc=True
            self.radio1.ack_delay=0.2
            self.radio1.sleep()
            self.radio1.node = self.cfg['id'] # our ID
            self.radio1.destination = self.cfg['gs'] # target's ID
            self.hardware['Radio1'] = True
            self.log('[INIT][Radio 1 - LoRa]')
        except Exception as e:
            self.log('[ERROR][INIT][Radio 1 - LoRa]: {}'.format(e))

        # init pib
        #TODO WIP
        try:
            self.rockblock_pw_sw = digitalio.DigitalInOut(board.PC07)
            self.rockblock_pw_sw.switch_to_output(value = False)
            self.rockblock_en = digitalio.DigitalInOut(board.PA19)
            self.rockblock_en.switch_to_output(value = False)
            self.pico_pw_sw = digitalio.DigitalInOut(board.PB17)
            self.pico_pw_sw.switch_to_output(value = False)
            self.pib = foras_promineo_pib.PIB(self)
            self.hardware['PIB'] = True
            self.log('[INIT][PIB]')
        except Exception as e:
            self.log('[ERROR][INIT][PIB]: {}'.format(e))

        #init startracker
        #TODO WIP
        try:
            pass
        except Exception as e:
            pass

        #init payload
        try:
            self.payload_pw_sw = digitalio.DigitalInOut(board.PC10)
            self.payload_pw_sw.switch_to_output(value = False)
            self.payload_rst = digitalio.DigitalInOut(board.PC06)
            self.payload_rst.switch_to_output(value = True)
            self.payload_servo_pwr_ctrl = digitalio.DigitalInOut(board.PC05)
            self.payload_servo_pwr_ctrl.switch_to_output(value=False)
            self.payload = foras_promineo_payload.PAYLOAD(self)
            self.hardware['PAYLOAD'] = True
            self.log('[INIT][PAYLOAD]')
        except Exception as e:
            self.log('[ERROR][INIT][PAYLOAD]: {}'.format(e))

        #init simulation class
        #TODO WIP
        try:
            self.sim = simulation.Simulation(self)
            self.log('[INIT][SIMULATION]')
        except Exception as e:
            self.log('[ERROR][INIT][SIMULATION]: {}'.format(e))

        # set PyCubed power mode # TODO CHANGE THIS FOR FP
        self.power_mode = 'normal'

    def reinit(self,dev):
        dev=dev.lower()
        if   dev=='gps':
            self.gps.__init__(self.uart,debug=self.debug)
        elif dev=='bus_pwr':
            self.bus_pwr.__init__(self.i2c1)
        elif dev=='chrg_pwr':
            self.chrg_pwr.__init__(self.i2c1)
        elif dev=='usb':
            self.usb.__init__(self.i2c1)
        elif dev=='imu':
            self.imu.__init__(self, 'IMU')
        elif dev=='pib':
            self.pib.__init__(self)
        elif dev=='payload':
            self.payload.__init__(self)
        else:
            self.log('Invalid Device? -> {}'.format(dev))

    @property
    def RGB(self):
        return self.neopixel[0]

    @RGB.setter
    def RGB(self,value):
        if self.hardware['Neopixel']:
            try:
                self.neopixel[0] = value
            except Exception as e:
                print('[WARNING]: {}'.format(e))

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
            _vbat=0
            for _ in range(50):
                _vbat+=self._vbatt.value * 3.3 / 65536
            _voltage = (_vbat/50)*(316+110)/110 # 316/110 voltage divider
            return _voltage # volts

    @property
    def system_voltage(self):
        if self.hardware['BUS_PWR']:
            try:
                return self.bus_pwr.read()[0] # volts
            except Exception as e:
                print('[WARNING][BUS PWR Monitor]: {}'.format(e))
        else:
            print('[WARNING][Bus Power monitor not initialized]')

    @property
    def current_draw(self):
        """
        current FROM batteries
        NOT accurate if powered via USB
        """
        if self.hardware['BUS_PWR']:
            idraw=0
            try:
                for _ in range(50): # average 50 readings
                    idraw+=self.bus_pwr.read()[1]
                return (idraw/50)*1000 # mA
            except Exception as e:
                print('[WARNING][BUS_PWR Monitor]: {}'.format(e))
        else:
            print('[WARNING] Bus Power monitor not initialized')

    # FIX this CH -- need to add charge current measurement on MB
    @property
    def charge_current(self):
        """
        current TO batteries FROM charger
        TODO WIP
        """
        if self.solar_charging:
            if self.hardware['CHRG_PWR']:
                try:
                    icharge=0
                    for _ in range(50):
                        icharge = self.chrg_pwr.read()[1]
                        return(icharge/50)*1000 # mA
                except Exception as e:
                    print('[WARNING][CHRG PWR Monitor]: {}'.format(e))
            else:
                print('[WARNING] CHRG Power monitor not initialized')
        else:
            return 0

    # look at this
    @property
    def batt_charge_current(self):
        return self.charge_current - self.current_draw

    # look at this
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
                print('vbus reset error?: {}'.format(e))
                pass
        self._resetReg.drive_mode=digitalio.DriveMode.PUSH_PULL
        self._resetReg.value=1

    def log(self, msg, print_flag=True):
        if self.hardware['SDcard']:
            with open(self.logfile, "a+") as f:
                t=int(time.monotonic())
                f.write('{}, {}\n'.format(t,msg))
        if print_flag: print(msg)

    def print_file(self,filedir=None,binary=False):
        if filedir==None:
            return
        print('\n--- Printing File: {} ---'.format(filedir))
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
        TODO needs edited for FP modes. norm and min modes should be removed from our application
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
                self.imu.powermode('min')
            if self.hardware['BUS_PWR']:
                self.bus_pwr.config('V_ONCE,I_ONCE')
            if self.hardware['CHRG_PWR']:
                self.chrg_pwr.config('V_ONCE,I_ONCE')
            if self.hardware['GPS']:
                self.en_gps.value = False
            if self.hardware['PIB']:
                self.pib.powermode('min')
            if self.hardware['PAYLOAD']:
                self.payload.powermode('min')
            self.power_mode = 'minimum'

        elif 'norm' in mode:
            #put neopixel here
            # put radio1 here
            self.enable_rf.value = True
            if self.hardware['IMU']:
                self.imu.powermode('norm')
            if self.hardware['BUS_PWR']:
                self.bus_pwr.config('V_CONT,I_CONT')
            if self.hardware['CHRG_PWR']:
                self.chrg_pwr.config('V_CONT,I_CONT')
            if self.hardware['GPS']:
                self.en_gps.value = True
            if self.hardware['PIB']:
                self.pib.powermode('norm')
            if self.hardware['PAYLOAD']:
                self.payload.powermode('norm')
            self.power_mode = 'normal'
            # don't forget to reconfigure radios, gps, etc...
            # EDIT THIS TO DO ABOVE CH- 4/6

        elif 'idle' in mode:
            pass

        elif 'safe' in mode:
            pass

        elif 'payload' in mode:
            pass

        elif 'startup' in mode:
            pass
        
    def new_file(self,substring,binary=False):
        '''
        substring something like '/data/DATA_'
        directory is created on the SD!
        int padded with zeros will be appended to the last found file
        '''
        if self.hardware['SDcard']:
            ff=''
            n=0
            _folder=substring[:substring.rfind('/')+1]
            _file=substring[substring.rfind('/')+1:]
            print('Creating new file in directory: /sd{} with file prefix: {}'.format(_folder,_file))
            try: chdir('/sd'+_folder)
            except OSError:
                print('Directory {} not found. Creating...'.format(_folder))
                try: mkdir('/sd'+_folder)
                except Exception as e:
                    print(e)
                    return None
            for i in range(0xFFFF):
                ff='/sd{}{}{:05}.txt'.format(_folder,_file,(n+i)%0xFFFF)
                try:
                    if n is not None:
                        stat(ff)
                except:
                    n=(n+i)%0xFFFF
                    # print('file number is',n)
                    break
            print('creating file...',ff)
            if binary: b='ab'
            else: b='a'
            with open(ff,b) as f:
                f.tell()
            chdir('/')
            return ff


    """
# is this not implemented in os.rm and os.rmdir? -CH
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

#what is the purpose of this? it is already implemented above... CH
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

#what is the purpose of this? the substring on new_file above creates directories -CH
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

#no current use for this/. imlemented in os.rmdir - CH
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

    # ------------------------------------------ Start Section modified by Marek Brodke on 12/8/2021
    """
# will be re-implemented in simulaton.py library. -CH
    def query_for_simulation(self, which):
        '''
        Sends a query for information to the computer connected to this one. This function requires tight integration with the software
        on the connected computer.

        :param which: what value to ask for from the connected computer

        :return: the data sent from the connected computer
        '''
        self.send_to_ground(b"GET_" + which)
        return eval(input())

# will be re-implemented in simulaton.py library. -CH
    def send_result_of_simulation(self, device, result):
        '''
        Sends the device name and the value that it would have been set to

        :param device: the name of the device that the value was sent to, can be anything as long it can be converted to a string
        :param result: the value sent the device with the inputted name
        
        :return: None
        '''
        self.send_to_ground("SET_{}{}".format(str(device), str(result)).encode("utf-8", 'w'))

#will be implemented in payload task or lib. -CH
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

# ? -CH
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

# ? -CH
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

# ? -CH
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

# ? -CH 
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
    """

    def i2c_rst(self):
        """
        I2C reset procedure

        >10 pulses on SCL @400khz to remove a hung-up bus

        TODO implement device-by-device re-init so self.i2c1.deinit() can run and then re-init all i2c devices.
        """
        #self.i2c1.deinit()
        scl = pwmio.PWMOut(board.SCL, duty_cycle=2**14, frequency=400000, variable_frequency=True)
        time.sleep(0.005) # >10 pusles
        scl.deinit()
        #self.i2c1 = busio.I2C(board.SCL,board.SDA, frequency=400000)

cubesat = Satellite()
