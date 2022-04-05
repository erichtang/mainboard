from Tasks.template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1/10 # once every 10s
    name = 'test'
    color = 'gray'

    schedule_later = True

    async def main_task(self):
        self.debug('test start: {}'.format(time.monotonic()))
        """
        read each IMU device
        """
        self.debug('\t GYRO0(dps): {}'.format(self.cubesat.imu.read('gyro0')))
        self.debug('\t GYRO1(dps): {}'.format(self.cubesat.imu.read('gyro1')))
        self.debug('\t MAG0(mG): {}'.format(self.cubesat.imu.read('mag0')))
        self.debug('\t MAG1(mG): {}'.format(self.cubesat.imu.read('mag1')))
        self.debug('\t ACCEL0(g): {}'.format(self.cubesat.imu.read('accel0')))
        self.debug('\t ACCEL1(g): {}'.format(self.cubesat.imu.read('accel1')))

        #await self.cubesat.tasko.sleep(10)
        self.debug('test stop: {}'.format(time.monotonic()))
