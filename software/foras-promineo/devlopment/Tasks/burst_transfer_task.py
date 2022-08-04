"""
TODO: verifiy all of this code. Some is unverified, some has been verified in previous implementations, best to debug it all.
task for managing large data transfers (<= chunk_size) between satellite subsystems 

NOTE:
    when LoRa is a source or destination for said file transfer, self.cubesat.secheduled_tasks['LoRa] should be STOPPED to avoid error
"""
from Tasks.template_task import Task
import time
import os
import payload_cmds as pl_cmds
import lora_cmds
import db_cmds

class task(Task):
    
    priority = 1
    frequency = 50
    name='burst_transfer'
    color = 'blue'

    chunk_size = 238

    

    def __init__(self, satellite):
        super().__init__(satellite)

        # self.burst_f = False
        # self.buffer_ready_f = False
        # self.chunk_i = 0
        # self.chunk_t = 0
        # self.source_size = 0
        # self.buffer_size = 0 # number of bytes filled in the buffer. 
        # self.source = ""
        # self.destination = ""
        # self.source_path = "" # only used for sd card source / destinations
        # self.destination_path = "" # only used for sd card source / destinations
        # self.t0 = 0
        # self.t1 = 0

        self.source_func_map = {
            # fill me in !
            'payload' : self.payload_source
        }

        self.destination_func_map = {
            # fill me in !
            'usb' : self.usb_destination
        }

    async def main_task(self):
        self.debug('asyn main')

        # self.debug(self.cubesat.burst_f)
        # self.debug(self.cubesat.buffer_ready_f)      
        self.debug(self.cubesat.source + 'srcs')         

        """
        check if burst mode is indicated on. this task only does something if it is.
        """
        if self.cubesat.burst_f:
            self.debug('bursting')

            if self.cubesat.buffer_ready_f:
                self.debug('usb dest')
                # send the buffer to the destination
                # this should be put in a try - except clause when it is working sufficiently!!!!
                self.destination_func_map[self.cubesat.destination]()

            else:

                self.debug('payload source')

                # fill the buffer from the source
                # this should be put in a try - except clause when it is working sufficiently!!!!
                self.source_func_map[self.cubesat.source]()

        else:
            self.debug('elsing')
            # after init, this task stops itself since it is only needed when a command is recieved.
            self.cubesat.scheduled_tasks[self.name].stop()
            
    def sd_source(self):

        # if this is the first chunk we are getting...
        if self.cubesat.chunk_i == 0:
            # get t0
            self.cubesat.t0 = time.monotonic_ns()
            # get size
            self.cubesat.source_size= os.stat(self.cubesat.source_path)[6]
            # calculate chunk_t
            self.chunk_calc()

        # calculate index to start read
        index = self.cubesat.chunk_i * self.chunk_size

        # calculate bytes2read
        if self.cubesat.chunk_i < self.cubesat.chunk_t - 1:
            bytes2read = self.chunk_size
        else: # bytes2read is different if this is the last chunk
            bytes2read = self.cubesat.source_size - (self.cubesat.chunk_i * self.chunk_size)
        
        # get the data
        with open(self.cubesat.source_path, 'rb') as f:
            #move pointer to current index
            f.seek(index)
            self.cubesat.send_buff[10:10+bytes2read] = f.read(bytes2read) # we start at the 10th index of this because it needs a 3 byte header for usb or a 10 byte header for radio...
            f.close()
        
        # flag that the buffer is ready to send on the next call of this task
        self.cubesat.buffer_ready_f = True
        # other flags and counters are altered at the end of the destination functions...

        # changing this to a name that makes sense for other functions to call.
        self.cubesat.buffer_size = bytes2read 

    def payload_source(self):
        self.debug('sdfghjkjhgfdsfghjk')
        
        self.debug(self.cubesat.chunk_t)

        self.debug('plsrs')

        if self.cubesat.chunk_i == 0:

            # get t0
            self.cubesat.t0 = time.monotonic_ns()

            # ask for photo size in bytes from payload with payload_cmds.request_picture_size
            # self.cubesat.source_size = pl_cmds.request_photo_size(self)

            # calculate chunks
            # self.chunk_calc()

        

        # request chunk from payload
        self.cubesat.buffer_size = pl_cmds.request_photo_chunk(self, self.cubesat.chunk_i) # this function will return the size of the data it puts in the buffer

        # self.debug(self.cubesat.buffer_size)

        # flag that the buffer is ready to send on the next call of this task
        self.cubesat.buffer_ready_f = True
        
        # other flags and counters are altered at the end of the destination functions...

    def usb_source(self):
        pass

    def lora_source(self):
        pass

    def payload_destination(self):
        pass

    def sd_destination(self):
        pass

    def payload_destination(self):
        pass

    def usb_destination(self):

        self.debug('usbdst')
        self.debug(self.cubesat.chunk_i)
        self.debug(self.cubesat.chunk_t)
        # if this is the first burst 
        if self.cubesat.chunk_i == 0:
            self.debug(self.cubesat.chunk_t)
            # call usb_cmds.write('BURST_START', self.cubesat.source_size)
            db_cmds.write('BURST_ST', self.cubesat.chunk_t.to_bytes(3,'big'))
            self.debug('chunk_i if pass')
            self.debug(self.cubesat.chunk_t)
            pass

        # send chunk 
        # call usb_cmds.write('BURST', self.cubesat.send_buff[:self.cubesat.buffer_size])
        self.debug(self.cubesat.buffer_size)
        # self.debug(self.cubesat.send_buff[10:10+self.cubesat.buffer_size])

        db_cmds.write('BURST_DATA', self.cubesat.send_buff[10:10+self.cubesat.buffer_size])

        # time.sleep(6)
        #reset flags for next chunk

        self.cubesat.buffer_ready_f = False     #is this the right flag?
        
        # if that was the last chunk
        if(self.cubesat.chunk_i == self.cubesat.chunk_t - 1):
            self.cubesat.burst_f = False
            self.cubesat.buffer_ready_f = False
            db_cmds.write('BURST_END')

            self.debug('7666666666666666666666666666666666666666666666666666666666666666666666666666666666666')
        self.cubesat.chunk_i += 1
        

    def lora_destination(self):
        """
        this destination selection blocks recieveing radio during burst downlink, be aware of that.
        those flags will have presumably been set by the function that declares a lora destination...
        """
        # if this is the first burst downlink
        if self.cubesat.chunk_i == 0:
            # assemble burst_start tx
            with self.cubesat.scheduled_tasks['LoRa'] as lora_task:
                burst_start_msg = lora_task.assemble_header(multiple_packets=True, length = self.cubesat.buffer_size, packet_number=self.cubesat.chunk_i, outof = self.cubesat.chunk_t+2)
            burst_start_msg += lora_cmds.tx['BURST_START']
            # send the burst start msg
            if not self.cubesat.radio1.send(burst_start_msg, keep_listening=False):
                self.debug("Burst Packet Tx FAIL") # temporary, this should raise an exception
            self.burst_start_debug()

        # assemble header for data
        with self.cubesat.scheduled_tasks['LoRa'] as lora_task:
                self.cubesat.send_buff[:10] = lora_task.assemble_header(multiple_packets=True, length = self.cubesat.buffer_size, packet_number=self.cubesat.chunk_i+1, outof = self.cubesat.chunk_t+2)
        # send the buffer
        if not self.cubesat.radio1.send(self.cubesat.send_buff[:self.cubesat.buffer_size], keep_listening=False):
                self.debug("Burst Packet Tx FAIL") # temporary, this should raise an exception
        # reset flags for next chunk
        self.cubesat.chunk_i += 1
        self.cubesat.buffer_ready_f = False

        # if that was the last chunk 
        if self.cubesat.chunk_i == self.cubesat.chunk_t:
            # assemble the burst_end cmd
            with self.cubesat.scheduled_tasks['LoRa'] as lora_task:
                burst_end_msg = lora_task.assemble_header(multiple_packets=True, length = self.cubesat.buffer_size, packet_number=self.cubesat.chunk_i+2, outof = self.cubesat.chunk_t+2)
            burst_end_msg += lora_cmds.tx['BURST_END']
            self.cubesat.radio1.send(burst_end_msg, keep_listening=True)

            self.cubesat.t1 = time.monotonic_ns() - self.cubesat.t0
            self.burst_end_debug()
            
            # reset variables and restart lora task
            self.burst_f = False
            with self.cubesat.scheduled_tasks['LoRa'] as lora_task:
                lora_task.start()
            
    def chunk_calc(self):
        self.cubesat.chunk_t =(self.cubesat.source_size // self.chunk_size) + (self.cubesat.source_size % self.chunk_size > 0)

    def burst_start_debug(self):
        self.debug("Burst Start")
        self.debug("{} to {}".format(self.cubesat.source, self.destination), 2)
        self.debug("{} bytes".format(self.cubesat.source_size), 2)

    def burst_end_debug(self):
        self.debug("Burst End")
        self.debug("{} ns elapsed".format(self.cubesat.t1), 2)

