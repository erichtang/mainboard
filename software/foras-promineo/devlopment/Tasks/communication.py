
"""
communication.py

communications via Irridium and LoRa Radios.

 need to implement something that avoids port timeout - MB

 WIP, i have not touched this. CH
"""
from Tasks.template_task import Task
import supervisor, time, struct, os

class task(Task):
    priority = 2
    frequency = 1
    name = 'communication to ground'

    def __init__(self, satellite):
        """
        Initialize the Task using the PyCubed cubesat object.
        
        :type satellite: Satellite
        :param satellite: The cubesat to be registered

        """
        self.cubesat = satellite

        self.connect_command = b"c___" # initializes connection between ground and this device, stops beacon

        # apply after connection has been made
        self.ground_commands = {b"p___" : self.ping, # ping command
                                b"pa__" : self.camera, # pings the camera and sends back if it responded
                                b"d___" : self.disconnect, # kills connection between ground and this device, starts beacon
                                b"l___" : self.get_log,
                                b"tel_" : self.get_telemetry,
                                b"cl__" : self.clear_log
                                }

        # value that is beaconed
        self.beacon_value = b"are you there"

        # a list of commands that can be sent from the ground
        self.ping_back_command = b"here"

        # holds the time of the last transmission from the ground
        self.last_transmission = 0

        # minutes to wait until stopping communicating from the ground and start beaconing again
        self.mintues_to_timeout = 1


    async def main_task(self):
        '''
        The main function for this class
        
        '''
        # temporary until radios are implemented
        self.cubesat.get_ground_into_buffer()

        # if connected to ground
        if self.cubesat.connected:
            if len(self.cubesat.buffer): # if something was read
                self.last_transmission = time.time() # setting the time since the last recieved transmission
                try: self.ground_commands[self.cubesat.buffer.get(0, 4)]() # running function in the dict
                except Exception as e : # if here then it is not a valid command, just ignores it
                    self.cubesat.send_to_ground(("Error in communication:"+str(e)).encode('utf-8'))

            else:
                # if too much time since the last transmission has pasted then start beaconing again
                if (time.time() - self.last_transmission)/60 > self.mintues_to_timeout: self.cubesat.connected = False
        
        else:
            # if recieved the command from the ground that starts the communication
            if len(self.cubesat.buffer) >= len(self.connect_command):
                if self.cubesat.buffer.get(0, len(self.connect_command)) == self.connect_command: self.connect()
            else:
                self.cubesat.buffer.write(self.beacon_value) # adds beacon value to the buffer
                self.cubesat.send_buffer_to_ground()


    def get_telemetry(self):
        # battery voltage = 2 bytes
        self.cubesat.buffer.write(b"TEL_")
        self.cubesat.buffer.append(struct.pack('f', self.cubesat.battery_voltage))
        self.cubesat.buffer.append(struct.pack('f', time.time() - self.cubesat.BOOTTIME))
        self.cubesat.send_buffer_to_ground()


    def clear_log(self):
        with open(self.cubesat.logfile, 'wb') as f:
            pass

    def get_log(self):
        self.cubesat.send_to_ground(b"generating log data")

        with open(self.cubesat.logfile, 'rb') as f:
            self.cubesat.buffer.write(b"LOG_")
            self.cubesat.buffer.append(f.read())
            self.cubesat.send_buffer_to_ground()

        self.cubesat.send_to_ground(b"done")


    def camera(self):
        '''
        processes camera commands

        '''
        if len(self.cubesat.buffer) >=8:
            # removing the comand that got us to this function from the buffer
            self.cubesat.buffer.pop(0, 4)

            # sends the rest of the data to the camera
            self.cubesat.send_buffer_to_camera()
            
            # the camera should respond to the above command, this respone is in the buffer
            self.cubesat.get_camera_into_buffer(timeout=1, clear_buffer_before=True) # listening for response for 10 seconds
            print(len(self.cubesat.buffer))
            # sends the result from the camera to the ground 
            self.cubesat.send_buffer_to_ground()


    def ping(self):
        '''
        Responds to recieving the ping command from the ground by sending back a command

        '''
        self.cubesat.buffer.write(self.ping_back_command)
        self.cubesat.send_buffer_to_ground()

    """
    def start_game(self):
        '''
        NOT YET IMPLEMENTED
        Sends the user's code to the camera which is run when is all recieved

        '''
        self.cubesat.send_to_camera(self.user_file_start_camera) # sends the command to the camera that indicates the user's code is coming
        f = open(self.cubesat.user_file_name, 'r') # opens the user's file for reading
        self.cubesat.send_to_camera(f.read().encode('utf-8')) # sends the lines of the file to camera in bytes form
        f.close()
        self.cubesat.game_is_running = True # sets flag that indicates the camera is playing the game

    
    def upload(self):
        '''
        NOT YET IMPLEMENTED
        Reads the users code upload from the communication bus
        
        '''
        #self.var = self.cubesat.get_ground() # getting the user code that is being sent
        
        f = open(self.cubesat.user_file_name, 'w') # opening the local user file for writing
        self.temp_file.write(self.var.decode('utf-8')) # writing the contents to the file after it is transformed from bytes to a string
        self.temp_file.close()
    """

    def disconnect(self):
        '''
        Responds to recieving the disconnect command by setting the flag that starts the beacon process
        
        '''
        self.cubesat.connected = False


    def connect(self):
        '''
        Function that is run when a connect command has been recieved
        
        '''
        self.cubesat.connected = True # tells the cubesat that it is connected to the ground
        
        # sending that connection has been achieved to the ground
        self.cubesat.buffer.write(b"Connected")
        self.cubesat.send_buffer_to_ground()
        self.last_transmission = time.time() # setting this so that a timeout can be calculated later on