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

# Disable RF and PYLD regulators,
enable_rf = digitalio.DigitalInOut(board.EN_RF)
enable_pyld = digitalio.DigitalInOut(board.EN_PYLD)
enable_rf.switch_to_output(value=False)
enable_pyld.switch_to_output(value=False)
print('[START][RF AND PAYLOAD REGULATORS DISABLED]')

# Initialize Neopixel
try:
    neopixel = neopixel.NeoPixel(
        board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
    neopixel[0] = (0, 256, 256)
    print('[START][Neopixel][PURPLE]')
except Exception as e:
    print('[ERROR][Neopixel]', e)

# Enable RF and PYLD regulators
enable_rf.value = True
enable_pyld.value = True
print('[START][RF AND PAYLOAD REGULATORS ENABLED]')

x=1
while x==1:
    time.sleep(25)
    print("[LOOP]")

print('[END]')
