"""
edits to the beepsat-advanced code 
not done, see ln 64 for changes to be made
may need aditional work as dev goes on.
ch 4/5/22
"""

from Tasks.template_task import Task
import msgpack
from os import stat
import time

SEND_DATA = False # make sure you have an antenna attached!

class task(Task):

    priority = 2
    frequency = 1/2 # during normal operation this would preform 2Hz, but is different for now.
    name = 'imu_sampler'
    color = 'green'

    # we want to initialize the data file only once upon boot
    # so perform our task init and use that as a chance to init the data files
    def __init__(self, satellite):
        super().__init__(satellite)
        self.data_file=self.cubesat.new_file('/data/imu',binary=True)
        self.cubesat = satellite

    async def main_task(self):

        # take IMU readings
        readings = {
            'gyro0_r'     : self.cubesat.imu.gyro0_r,
            'gyro0_t'     : self.cubesat.imu.gyro0_t, #_t suffix means temperature
            'gyro1_r'     : self.cubesat.imu.gyro1_r,
            'gyro1_t'     : self.cubesat.imu.gyro1_t,
            'mag0_r'      : self.cubesat.imu.mag0_r,
            'mag0_t'      : self.cubesat.imu.mag0_t,
            'mag1_r'      : self.cubesat.imu.mag1_r,
            'mag1_t'      : self.cubesat.imu.mag1_t,
            'accel0_r'    : self.cubesat.imu.accel0_r,
            'accel0_t'    : self.cubesat.imu.accel0_t,
            'accel1_r'    : self.cubesat.imu.accel1_r,
            'accel1_t'    : self.cubesat.imu.accel1_t,
            'timestamp'   : (time.time()-self.cubesat.BOOTTIME), #time since boot of measurement
        }
        if self.cubesat.hardware['PAYLOAD']:
            #if self.cubesat.payload.hardware['imu']:
                #append readings dict to add payload 
            pass

        # store them in our cubesat data_cache object
        self.cubesat.data_cache.update({'imu':readings})

        # print the readings with some fancy formatting
        self.debug('IMU readings (x,y,z), dps, mG, g')
        for imu_type in self.cubesat.data_cache['imu']:
            self.debug('{:>5} {}'.format(imu_type,self.cubesat.data_cache['imu'][imu_type]),2)
        pass

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
                """
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
                """
                self.data_file=self.cubesat.new_file('/data/imu')

    
