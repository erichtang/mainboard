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
import pca9543
import iam20380
import mmc5983
import mxc6655

from micropython import const

print('[START]')

# Define SPI,I2C,UART
i2c1 = busio.I2C(board.SCL, board.SDA)
spi = board.SPI()
uart1 = busio.UART(board.TX, board.RX)
uart2 = busio.UART(board.TX2, board.RX2)
uart3 = busio.UART(board.TX3, board.RX3)
uart4 = busio.UART(board.TX4, board.RX4)
#print('[SERIAL PORTS INITIALIZED]')

# Disable RF and PYLD regulators,
enable_rf = digitalio.DigitalInOut(board.EN_RF)
enable_pyld = digitalio.DigitalInOut(board.EN_PYLD)
enable_rf.switch_to_output(value=False)
enable_pyld.switch_to_output(value=False)
#print('[START][RF AND PAYLOAD REGULATORS DISABLED]')

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

mux = pca9543.PCA9543(i2c1, mux_addr)
mux.set_ch0()

gyro = iam20380.IAM20380(i2c1, gyro_addr)
magm = mmc5983.MMC5983(i2c1, mag_addr)
accel = mxc6655.MXC6655(i2c1, accel_addr)
time.sleep(0.01)
gyro_m = gyro.read()
magm_m = magm.read()
accel_m = accel.read()

x=0

print ("[GYRO]",gyro.read())
print("[GYRO]",gyro.temp())
print ("[MAG]",magm.read())
print ("[MAG]",magm.temp())
print ("[ACCEL]",accel.read())
print ("[ACCEL]",accel.temp())

# I2C Scan
# try:
#     print("[I2C_SCAN][START]")
#     i2c1.try_lock()
#     print(
#         "[I2C addresses found:][MUX DISABLED]",
#         [hex(device_address) for device_address in i2c1.scan()],
#     )
#     i2c1.unlock()
# except Exception as e:
#     print('[ERROR][I2C_SCAN]', e)

print('[END]')
