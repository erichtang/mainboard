"""
CircuitPython PyCubed Basic Board Evaluation

    1. Detects Devices on I2C bus
    2. Detects Devices on SPI busses
    3. Detects Devices on UART busses
    4. Enables payload and RF regulators for testing
    5. Blinks NeoPixel on main loop reset
    update this

C. Hillis 03/13/22

"""

# Common CircuitPython Libs
import board
import microcontroller
import busio
import time
import sys
from storage import mount, umount, VfsFat
from analogio import AnalogIn
import digitalio
import sdcardio
import pwmio

# Hardware Specific Libs
import pycubed_rfm9x  # Radio
import neopixel  # RGB LED
import bq25883  # USB Charger
import adm1176  # Power Monitor
import pycubed_imu

from micropython import const

print('[START]')

# Define SPI,I2C,UART
i2c1 = busio.I2C(board.SCL, board.SDA)
spi = board.SPI()
uart1 = busio.UART(board.TX, board.RX)
uart2 = busio.UART(board.TX2, board.RX2)
uart3 = busio.UART(board.TX3, board.RX3)
uart4 = busio.UART(board.TX4, board.RX4)
print('[SERIAL PORTS INITIALIZED]')

# Disable RF and PYLD regulators,
enable_rf = digitalio.DigitalInOut(board.EN_RF)
enable_pyld = digitalio.DigitalInOut(board.EN_PYLD)
enable_rf.switch_to_output(value=False)
enable_pyld.switch_to_output(value=False)
print('[START][RF AND PAYLOAD REGULATORS DISABLED]')

# Enable RF and PYLD regulators
enable_rf.value = True
enable_pyld.value = True
print('[START][RF AND PAYLOAD REGULATORS ENABLED]')

# Initialize SD Card
#       Baud rate depends on the card, 4MHz should be safe
try:
    sd = sdcardio.SDCard(spi, board.SD_CS, baudrate=4000000)
    vfs = VfsFat(sd)
    mount(vfs, "/sd")
    fs = vfs
    sys.path.append("/sd")
    print('[START][SDcard][INIT]')
    logfile = "/sd/log.txt"
except Exception as e:
    print('[ERROR][SD Card]', e)

# Initialize Neopixel
try:
    neopixel = neopixel.NeoPixel(
        board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
    neopixel[0] = (0, 120, 120)
    print('[START][Neopixel][PURPLE]')
except Exception as e:
    print('[ERROR][Neopixel]', e)

# Initialize ADC
try:
    vbatt = AnalogIn(board.BATTERY)
    print('[START][ADC]')
    print('[BATTERY][VOLTAGE]', vbatt)
except Exception as e:
    print('[ERROR][ADC]')

# Initialize USB charger
try:
    usb = bq25883.BQ25883(i2c1, addr=0x4A)
    usb.charging = False
    usb.wdt = False
    usb.led = False
    usb.charging_current = 8  # 400mA
    usb_charging = False
    print('[START][USB_CHARGER][DISABLED]')
except Exception as e:
    print('[ERROR][USB_CHARGER]', e)

# Initialize Power Monitor
try:
    pwr = adm1176.ADM1176(i2c1)
    pwr.sense_resistor = 0.1
    print('[START][POWER_MONITOR]')
    print('[POWER_MONITOR][CURRENT][{pwr}]')
except Exception as e:
    print('[ERROR][POWER_MONITOR]', e)

# Initalize GPS
try:
    en_gps = digitalio.DigitalInOut(board.EN_GPS)
    en_gps.switch_to_output()
    print('[START][GPS]')
except Exception as e:
    print('[ERROR][GPS]', e)

# Define radio
rf_cs1 = digitalio.DigitalInOut(board.RF1_CS)
rf_rst1 = digitalio.DigitalInOut(board.RF1_RST)
radio1_DIO0 = digitalio.DigitalInOut(board.RF1_IO0)
# self.enable_rf.switch_to_output(value=False) # if U21
enable_rf.value = True  # if U7
rf_cs1.switch_to_output(value=True)
rf_rst1.switch_to_output(value=True)
radio1_DIO0.switch_to_input()
# Initalize Radio 1
try:
    radio1 = pycubed_rfm9x.RFM9x(spi, rf_cs1, rf_rst1,
                                 433.0, code_rate=8, baudrate=1320000)
    # Default LoRa Modulation Settings
    # Frequency: 433 MHz, SF7, BW125kHz, CR4/8, Preamble=8, CRC=True
    radio1.dio0 = radio1_DIO0
    radio1.enable_crc = True
    radio1.ack_delay = 0.2
    radio1.sleep()
    print('[START][RADIO_1]')
    print('[RADIO_1][SLEEP]')
except Exception as e:
    print('[ERROR][RADIO 1]', e)

# Initalize Radio 2
    # not implemented

# # Initalize IMU
mux_addr = 0x70
gyro_addr = 0x69
accel_addr = 0x30
mag_addr = 0x15
try:
    imu0 = pycubed_imu.imu(i2c1, mux_addr, gyro_addr, accel_addr, mag_addr)
    print('[START][IMU]')
except Exception as e:
    print('[ERROR][IMU]', e)

# I2C Scan
try:
    print("[I2C_SCAN][START]")
    i2c1.try_lock()
    print(
        "[I2C addresses found:][MUX DISABLED]",
        [hex(device_address) for device_address in i2c1.scan()],
    )
    i2c1.unlock()
except Exception as e:
    print('[ERROR][I2C_SCAN]', e)

print('[END]')
