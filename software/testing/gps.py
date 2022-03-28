"""
CircuitPython PyCubed Basic Board Evaluation


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
import adafruit_gps

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

# Initialize Neopixel
try:
    neopixel = neopixel.NeoPixel(
        board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
    neopixel[0] = (0, 120, 120)
    print('[START][Neopixel][PURPLE]')
except Exception as e:
    print('[ERROR][Neopixel]', e)

# Initalize GPS
try:
    en_gps = digitalio.DigitalInOut(board.EN_GPS)
    en_gps.switch_to_output(value=True)
    print('[PWR][GPS]')
    time.sleep(2)
    print("[BOOT][GPS")
    gps = adafruit_gps.GPS(uart1, debug=True) # Enable debugging to see raw GPS output

    last_print = time.monotonic()
    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        while not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...be patient!')
            time.sleep(0.5)
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,   # month!
            gps.timestamp_utc.tm_sec))
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Fix quality: {}'.format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.altitude_m is not None:
            print('Altitude: {} meters'.format(gps.altitude_m))
        if gps.speed_knots is not None:
            print('Speed: {} knots'.format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print('Track angle: {} degrees'.format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print('Height geo ID: {} meters'.format(gps.height_geoid))
except Exception as e:
    print('[ERROR][GPS]', e)

print('[END]')
