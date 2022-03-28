"""
`imu_print_data_serial_host.py`
====================================================
reading pycubed serial IMU data and calculating noise / maybe visualization



* Author(s):  C. Hillis

--------------------

"""
import time
import serial
import sys


# main loop
while True:
    #wait/get serial data
    with serial.Serial('COM8', 115200, timeout=1) as ser:
        #loook for % signalling new measurement
        ser.open()
        serial_in = [0]
        while(serial_in[0] != '%'):
            serial_in = ser.readline()
            print("waiting for %")
    
    #time to massage relevant data out, this will certianly NOT be painless
        



