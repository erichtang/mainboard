"""
Serial CLI program as an example test radio interface for foras promineo

"""

import serial
import threading
import time

cmd_codes = {
    'no-op' : b'\x8eb',
    'hreset' : b'\xd4\x9f',
    'shutdown' : b'\x12\x06',
    'query' : b'8\x93',
    'exec_cmd' : b'\x96\xa2',
    'connect' : b'\xf0',
    'burst_test': b'ab'
}

#serial and file
ser = serial.Serial('COM11', 115200, timeout=0)
#ser.open()
logfile = open("serial_log.txt", "w", encoding = "utf-8")

#function def's
def serial_data_getter():
    while True:
        if ser.in_waiting:
            rx_data = ser.read(1023) # radio packets are ~248, the radio interface adds 34 bytes of char 300 for margin
            while len(rx_data) > 10:
                try:
                    #print(rx_data)
                    start_seq = ("RX START :::").encode("utf-8")
                    endmsg_seq = ("::: RX END\r\n").encode("utf-8")
                    rssi_seq = ("RSSI: ").encode("utf-8")
                    end_seq = ("\r\n").encode("utf-8")
                    start_i = rx_data.find(start_seq)
                    endmsg_i = rx_data.find(endmsg_seq, start_i)
                    rssi_i = rx_data.find(rssi_seq, endmsg_i)
                    end_i = rx_data.find(end_seq, rssi_i)
                    msg = rx_data[start_i + len(start_seq) : endmsg_i]
                    header = msg[:10]
                    msg = msg[10:]
                    #print(header)
                    print(msg)
                    rssi = rx_data[rssi_i + len(rssi_seq) : end_i]
                    #print(rssi)
                    rx_data = rx_data[end_i:]
                except Exception as e:
                    print(e)
        time.sleep(1)

def end():
    ser.close()
    logfile.close()
    quit()

# this is where the execution actually starts

# having gatherer thread run in backround
threading1 = threading.Thread(target=serial_data_getter)
threading1.daemon = True
threading1.start()

while True:
    usr_input = input() # this will stay here untill something is put in
    cmd = cmd_codes[usr_input]
    b =  len(cmd) + 10  # serial radio requires a 1 byte to know how long the mesg it is going to send will be
    h = b"code\x00\x00\x00\x00\x00\x00"
    msg2send = bytearray(b)
    msg2send[0] = b
    msg2send[1:11] = h
    msg2send[11:] = cmd
    ser.write(msg2send)
    time.sleep(.1)
