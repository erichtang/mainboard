"""

C. Hillis 03/23/22

"""

# Common CircuitPython Libs
import board
import microcontroller
import busio
import time
import sys
import digitalio

# Hardware Specific Libs
import neopixel  # RGB LED
import pycubed_imu as imu

from micropython import const

print('[START]')

# Define SPI,I2C,UART
i2c1 = busio.I2C(board.SCL, board.SDA)

# Disable RF and PYLD regulators,
enable_rf = digitalio.DigitalInOut(board.EN_RF)
enable_pyld = digitalio.DigitalInOut(board.EN_PYLD)
enable_rf.switch_to_output(value=False)
enable_pyld.switch_to_output(value=False)

# Initialize Neopixel
try:
    neopixel = neopixel.NeoPixel(
        board.NEOPIXEL, 1, brightness=0.2, pixel_order=neopixel.GRB)
    neopixel[0] = (0, 120, 120)
    #print('[START][Neopixel][PURPLE]')
except Exception as e:
    #print('[ERROR][Neopixel]', e)
    x=1

# # Initalize IMU
mux_addr = 0x70
gyro_addr = 0x69
accel_addr = 0x15
mag_addr = 0x30
buffer_length = 1
imu0 = imu.IMU(i2c1, mux_addr, gyro_addr, accel_addr, mag_addr, buffer_length)

x=0
while (x < 100):
    imu0.read()
    print("%", imu0.gyro_data, imu0.mag_data, imu0.accel_data, imu0.temp_data)
    x+=1
    time.sleep(1)

print('[END]')
