"""
TODO -- foras promineo payload devlopment is still onging. this is a first pass. This task is currently ignored

this task currently (unverified-ily) handles getting photo chunks from the openMV camera and putting them in a buffer for lora_task.py to beam down.
not of this is verified to work, but is code of how i imagine it would operate.

maybe the larhe packet can be generalized so other things can transmit larger amounts of data? i.e. a log file IDK
"""
from Tasks.template_task import Task
import time

class task(Task):
    
    priority = 2
    frequency = 30
    name='payload'
    color = 'green'

    async def main_task(self):
        """
        if we are in image burst mode, get next chunk of image and flag that it send is ready
        """
        if self.cubesat.payload.img_bst_flag:
            if not self.cubesat.payload.send_buff_flag:
                # ask for the next packet from openmv
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


