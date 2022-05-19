"""
attidude control task:

FSM running all attitude control related data handling and execution


"""


from Tasks.template_task import Task
import time
class task(Task):
    priority = 2
    frequency = 1
    name = 'attitude_control'

    async def main_task(self):
        pass
        '''
        # Read acceleration, magnetometer, gyroscope, temperature.
        temp = self.cubesat.temperature
        accel_x, accel_y, accel_z = self.cubesat.acceleration
        mag_x, mag_y, mag_z       = self.cubesat.magnetic
        gyro_x, gyro_y, gyro_z    = self.cubesat.gyro

        # Print values.
        self.cubesat.send_to_ground('Temperature: {}C'.format(temp).encode('utf-8'))
        self.cubesat.send_to_ground('Acc  (m/s^2):   x: {}\ty: {}\tz: {}'.format(accel_x, accel_y, accel_z).encode('utf-8'))
        self.cubesat.send_to_ground('Mag     (uT):   x: {}\ty: {}\tz: {}'.format(mag_x, mag_y, mag_z).encode('utf-8'))
        self.cubesat.send_to_ground('Gyro (deg/sec): x: {}\ty: {}\tz: {}'.format(gyro_x, gyro_y, gyro_z).encode('utf-8'))

        # Delay for a second.
        time.sleep(1)
        '''