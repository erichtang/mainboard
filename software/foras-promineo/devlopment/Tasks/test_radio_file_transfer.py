"""

"""
from Tasks.template_task import Task
import time
import os

class task(Task):
    
    priority = 2
    frequency = 100
    name='file transfer'
    color = 'blue'

    max_packet_len = 242

    async def main_task(self):
        """
        if we are in image burst mode, get next chunk of file and flag that it send is ready
        """
        if self.cubesat.radio1_burst_flag and not self.cubesat.send_buff_flag: 
            
            if self.cubesat.brst_pkt_num == 0: # do some more things if this is the first packet we are grabbing
                #get file size
                self.cubesat.file_downlink_size = os.stat(self.cubesat.file_downlink_path)[6]
                #figure out no. of packets we are sending
                self.cubesat.brst_pkt_tot = (self.cubesat.file_downlink_size // 242) + (self.cubesat.file_downlink_size % 252 > 0)

            #figure out how many bytes to read at what index
            index = self.cubesat.brst_pkt_num * self.max_packet_len
            if self.cubesat.brst_pkt_num < self.cubesat.brst_pkt_tot:
                bytes2read = self.max_packet_len
            else:
                bytes2read = (self.cubesat.brst_pkt_tot * self.max_packet_len) - self.cubesat.file_downlink_size
            
            #get the data
            with open(self.file_downlink_path, 'rb') as f:
                #move pointer to current index
                self.cubesat.send_buf[10:] = 


                self.cubesat.uart2.write(self.cubesat.payload.cmd_dispatch['next_pkt'])
                bytes_rx = self.cubesat.uart2.readinto(self.cubesat.payload.buf)
                self.debug("Data chunk recieved from payload:")
                self.debug("{}".format(self.cubesat.payload.buf_read), 2)
                if bytes_rx == 244: # if correct number of bytes recieved
                    self.cubesat.payload.send_buff_flag = True
                elif bytes_rx < 244: # if less than correct number
                    if self.cubesat.payload.read_buf[2:3] == self.cubesat.payload.read_buf[4:5]: # if it is the last chunk
                        self.cubesat.payload.buf[247:248] = b'0xffff' #assign the end flag
                        self.debug("End of photo burst detected :)")
                        self.cubesat.payload.send_buff_flag = True
                    else:
                        self.debug("Invalid data from payload durng burst")


