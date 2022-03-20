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
import digitalio

# Hardware Specific Libs
import neopixel  # RGB LED
import iam20380
import pca9543

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

# # Initalize IMU
mux_addr = 0x70
gyro_addr = 0x69
accel_addr = 0x30
mag_addr = 0x15
try:
    mux = pca9543.PCA9543(i2c1, mux_addr)
    mux.set_ch0()
    gyro = iam20380.IAM20380(i2c1, gyro_addr)
    test = gyro.fs_sel
    gyro.fs_sel = test
    print('[START][GYRO]')
except Exception as e:
    print('[ERROR][IMU]', e)
