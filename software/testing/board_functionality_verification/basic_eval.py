"""
CircuitPython PyCubed Board Evaluation

C. Hillis 03/02/22

"""

print('[START]')
# Common CircuitPython Libs
import board, microcontroller
import busio, time, sys
from storage import mount,umount,VfsFat
from analogio import AnalogIn
import digitalio, sdcardio, pwmio

# Define SPI,I2C,UART
i2c  = busio.I2C(board.SCL,board.SDA)
spi   = board.SPI()
uart1  = busio.UART(board.PB02,board.PB03) #tx,rx uart 1 may have to be redefined in firmware
uart2  = busio.UART(board.PA17,board.PA16)
uart3  = busio.UART(board.PC13,board.PC12)
uart4  = busio.UART(board.PC17,board.PC16)

# Initialize SD Card
#       Baud rate depends on the card, 4MHz should be safe
try:
    sd = sdcardio.SDCard(spi, board.SD_CS, baudrate=4000000)
    vfs = VfsFat(sd)
    mount(vfs, "/sd")
    fs=vfs
    sys.path.append("/sd")
    print('[SDcard] = True')
    logfile="/sd/log.txt"
except Exception as e:
    print('[ERROR][SD Card]',e)

# Initialize Neopixel
try:
    neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
    neopixel[0] = (0,0,0)
    print('[Neopixel] = True)')
except Exception as e:
    print('[WARNING][Neopixel]',e)

vbatt = AnalogIn(board.BATTERY)
print('[BATTERY][VOLTAGE]', vbatt)

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
    if self.debug: print('[ERROR][USB Charger]',e)

# Initialize Power Monitor
try:
    pwr = adm1176.ADM1176(self.i2c1)
    pwr.sense_resistor = 0.1
    print('[Start]')
    ][Power Monitor]'] = True
except Exception as e:
    print('[ERROR][Power Monitor]',e)


print('[END]')