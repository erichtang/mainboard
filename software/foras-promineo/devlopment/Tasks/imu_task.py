"""
imu_sampler.py

edits to the beepsat-advanced code 

not done
may need aditional work as dev goes on.

have it try to fix an error'd out imu device every hour

ch 4/5/22
"""

from Tasks.template_task import Task
import msgpack
from os import stat
import time

SEND_DATA = False # make sure you have an antenna attached!

class task(Task):

    priority = 2
    frequency = 1 #other tasks will probably adjust this
    name = 'imu'
    color = 'green'

    # we want to initialize the data file only once upon boot
    # so perform our task init and use that as a chance to init the data files
    def __init__(self, satellite, samples=10):
        #self.data_file=self.cubesat.new_file('/data/imu',binary=True) # why does this take so long?
        self.cubesat=satellite
        self.samples=samples



    async def main_task(self):
        
        # take IMU readings 

        #big readings dict, 8byte float * 12 * 3 
        readings = { 
            'gyro'  : [None]*4,
            'mag'   : [None]*4,
            'accel' : [None]*4,
            'timestamp'  : None, #time since boot of measurement
        }

        if self.cubesat.hardware['IMU']:
                readings['gyro'][0] = self.oversampler(self.cubesat.imu.gyro0)
                readings['gyro'][1] = self.oversampler(self.cubesat.imu.gyro1)
                readings['mag'][0] = self.oversampler(self.cubesat.imu.mag0)
                readings['mag'][1] = self.oversampler(self.cubesat.imu.mag1)
                readings['accel'][0] = self.oversampler(self.cubesat.imu.accel0)
                readings['accel'][1] = self.oversampler(self.cubesat.imu.accel1)
        if self.cubesat.hardware['PIB']:
            if self.cubesat.pib.hardware['IMU']:
                readings['gyro'][2] = self.oversampler(self.cubesat.pib.imu.gyro0)
                readings['gyro'][3] = self.oversampler(self.cubesat.pib.imu.gyro1)
                readings['mag'][2] = self.oversampler(self.cubesat.pib.imu.mag0)
                readings['mag'][3] = self.oversampler(self.cubesat.pib.imu.mag1)
                readings['accel'][2] = self.oversampler(self.cubesat.pib.imu.accel0)
                readings['accel'][3] = self.oversampler(self.cubesat.pib.imu.accel1)

        readings['timestamp']= (time.time()-self.cubesat.BOOTTIME)

        self.cubesat.data_cache.update({'imu':readings})

        # print the readings with some fancy formatting
        self.debug('IMU readings (x,y,z), dps, uT, g')
        for imu_type in self.cubesat.data_cache['imu']:
            self.debug('{:>5} {}'.format(imu_type,self.cubesat.data_cache['imu'][imu_type]),2)
        pass

        """
        # save data to the sd card, but only if we have a proper data file
        if self.data_file is not None:
            # save our readings using msgpack
            with open(self.data_file,'ab') as f:
                msgpack.pack(readings,f)
                self.debug("Data File Size: {}".format(stat(self.data_file)[6])) # prints number of bytes the filesize is [it *is 16*(number of dict keys)] currently 215bytes

        
            # check if the file is getting bigger than we'd like
            '''
            possibly edit this to save a larger file?
            this will not send data as long as dend_data is false 
                but the transmit of this data needs to be moved to a different task and execute under different conditions
            '''
            if stat(self.data_file)[6] >= 256: # bytes
                #
                if SEND_DATA:
                    print('\nSend IMU data file: {}'.format(self.data_file))
                    with open(self.data_file,'rb') as f:
                        chunk = f.read(64) # each IMU readings is 64 bytes when encoded
                        while chunk:
                            # we could send bigger chunks, radio packet can take 252 bytes
                            self.cubesat.radio1.send(chunk)
                            print(chunk)
                            chunk = f.read(64)
                    print('finished\n')
                '''
                data is already printed with line 57
                edited out for now
                else:
                    # print the unpacked data from the file
                    print('\nPrinting IMU data file: {}'.format(self.data_file))
                    with open(self.data_file,'rb') as f:
                        while True:
                            try: print('\t',msgpack.unpack(f))
                            except: break
                    print('finished\n')
                # increment our data file number
                '''
                self.data_file=self.cubesat.new_file('/data/imu')
        """
    
    def oversampler(self, ptr):
        i=0
        avg = self.samples
        temp = [0,0,0]
        while i < self.samples:
            temp2 = ptr
            try:
                for axis in range(len(temp)):
                    temp[axis] += temp2[axis]
            except:
                avg -= 1
            i += 1
        for axis in range(len(temp)):
            if temp[axis] is not None and temp[axis] > 0: 
                temp[axis] /= avg
                return temp
        