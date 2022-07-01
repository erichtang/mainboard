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
        if self.cubesat.radio1_burst_flag and not self.cubesat.send_buff_ready_flag: 
            
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
                f.seek(index)
                self.cubesat.send_buf[10:] = f.read(bytes2read)
                f.close()
            
            #flag to the lora task that this is ready to send
            self.cubesat.send_buff_ready_flag = True



