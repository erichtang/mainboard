from Tasks.template_task import Task
import time

class task(Task):
    """
    TODO: need to add functionality where this class is supended until the command from the ground is recieved
    
    """

    priority = 4
    frequency = 5
    name = 'cam'

    command_to_get_frame = b"send"
    
    frame_time = 1/5 # time between frames to grab from the camera, the denominator is the fps
    last_frame_time = 0

    image = None

    async def main_task(self):
        if self.cubesat.game_is_running:
            if time.monotonic() - self.last_frame_time >= self.frame_time: # if the time since the last frame is greater than the allotted time
                self.cubesat.send_to_camera(self.command_to_get_frame) # sending the command to main flight computer
                self.image = self.cubesat.get_camera(timeout=1) # reading the image and waiting a little longer because the camera has to do some processing

                if self.image is not None:
                    self.cubesat.send_to_ground(self.image) # sends the image to the ground
                    self.image = None # erasing the image so it does not hang around for long
                    self.last_frame_time = time.monotonic() # setting the last frame time marker for the next iteration
                
                else:
                    self.cubesat.game_is_running = False # if there was no image recieved then the camera is no loger running the user's code