"""
lora rx test
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
import pycubed_rfm9x  # Radio
import neopixel  # RGB LED

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
                                 433.0, code_rate=5, baudrate=1320000)
    # Default LoRa Modulation Settings
    # Frequency: 433 MHz, SF7, BW125kHz, CR4/8, Preamble=8, CRC=True
    radio1.dio0 = radio1_DIO0
    radio1.enable_crc = True
    radio1.ack_delay = 0.2
    radio1.spreading_factor = 7
    radio1.enable_crc = True
    radio1.code_rate = 5
    radio1.sleep()
    print('[START][RADIO_1]')
    print('[RADIO_1][SLEEP]')
    time.sleep(1)
    print('[RADIO_1]')
    l = 0
    while l < 1000:
        rx = radio1.receive()
        print("Data recieved:")
        print(rx)
        l +=1
except Exception as e:
    print('[ERROR][RADIO 1]', e)

print('[END]')
