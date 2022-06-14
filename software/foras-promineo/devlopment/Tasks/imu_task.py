"""
imu_sampler.py

edits to the beepsat-advanced code 

TODO add a mode setting where the task can be configured to use any 2 imu devices. have this task turn the unused IMU devices OFF.

ch 4/5/22
"""

from Tasks.template_task import Task
import time

class task(Task):

    #priority = 2
    #frequency = 1 #other tasks will probably adjust this
    name = 'imu'
    color = 'green'

    d_cfg = {
        'priority' : 2,
        'frequency' : 1,
        'imu_sel' : 2, # 0 for mainboard imu, 1 for pib imu, 2 for both
        'samples' : 5
    }

    # we want to initialize the data file only once upon boot
    # so perform our task init and use that as a chance to init the data files
    def __init__(self, satellite):
        #self.data_file=self.cubesat.new_file('/data/imu',binary=True) # why does this take so long?
        self.cubesat=satellite

        self.cfg = self.d_cfg
        self.load_cfg(self.cfg, self.name)


    async def main_task(self):
        
        # take IMU readings 

        #big readings dict, 8byte float * 12 * 3 
        readings = { 
            'gyro'  : [],
            'mag'   : [],
            'accel' : [],
            'timestamp'  : None, #time since boot of measurement
        }

        if self.cfg['imu_sel'] == 0 or self.cfg['imu_sel'] == 2: # mainboard imu
            if self.cubesat.hardware['IMU']:
                readings['gyro'].append(self.oversampler(self.cubesat.imu.gyro0))
                readings['gyro'].append(self.oversampler(self.cubesat.imu.gyro1))
                readings['mag'].append(self.oversampler(self.cubesat.imu.mag0))
                readings['mag'].append(self.oversampler(self.cubesat.imu.mag1))
                readings['accel'].append(self.oversampler(self.cubesat.imu.accel0))
                readings['accel'].append(self.oversampler(self.cubesat.imu.accel1))
        elif self.cfg['imu_sel'] == 1 or self.cfg['imu_sel'] == 2: # pib imu
            if self.cubesat.hardware['PIB']:
                if self.cubesat.pib.hardware['IMU']:
                    readings['gyro'].append(self.oversampler(self.cubesat.pib.imu.gyro0))
                    readings['gyro'].append(self.oversampler(self.cubesat.pib.imu.gyro1))
                    readings['mag'].append(self.oversampler(self.cubesat.pib.imu.mag0))
                    readings['mag'].append(self.oversampler(self.cubesat.pib.imu.mag1))
                    readings['accel'].append(self.oversampler(self.cubesat.pib.imu.accel0))
                    readings['accel'].append(self.oversampler(self.cubesat.pib.imu.accel1))

        readings['timestamp']= (time.time()-self.cubesat.BOOTTIME)

        self.cubesat.data_cache.update({'imu':readings})

        # print the readings with some fancy formatting
        self.debug('IMU readings (x,y,z), dps, uT, g')
        for imu_type in self.cubesat.data_cache['imu']:
            self.debug('{:>5} {}'.format(imu_type,self.cubesat.data_cache['imu'][imu_type]),2)
        pass
    
    def oversampler(self, ptr):
        i=0
        avg = self.cfg['samples']
        temp = [0,0,0]
        while i < self.cfg['samples']:
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
        