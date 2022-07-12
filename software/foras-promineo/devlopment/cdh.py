"""
radio transmit and recieve commands.

radio recieves the following packet structure:

10 bytes header
2 bytes cmd code
x bytes after are args to the command.

args formatting is defined on a per-command basis.
"""
import time

"""
    2-byte command codes of recieved commands here
"""
rx = {
    b"\x8eb" : "no_op",
    b'\xd4\x9f': 'hreset',
    b'\x12\x06': 'shutdown',
    b'8\x93': 'query',
    b'\x96\xa2': 'exec_cmd',
    b'\xf0' : 'connect',
    b'ab' : 'burst_test'
}

tx = {
    """
    2-byte command codes of transmitted commands here
    """
    "NACK" : b"\xFF\xFF",
    "ACK"  : b"\xAA\xC1",
    "ERROR": b"\xEE\xEE",
    "BEACON": b"\xbe\xac",
    "BRST_ST": b"BS",
    "BRST_END": b"BE",
}

########### commands without arguments ###########
def noop(self):
    """
    Returns ACK via radio 
    """
    self.debug('no-op command recieved')
    self.cubesat.radio1.send(tx['ACK'])
    pass

def hreset(self):
    """
    Hard resets the satellite.
    """
    self.debug('Resetting')
    try:
        self.cubesat.radio1.send(data=b'resetting')
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        pass

def connect(self): 
    """
    initates the radio "connected" state
    """
    pass

def disconnect(self):
    """
    deinitiates the radio "connected" state
    """
    pass

def print_telemetry(self):
    """
    transmits important telemetry down to the ground
    """
    pass

def download_log(self):
    """
    transmits logfile down to the ground
    """
    pass

########### commands with arguments ###########

def shutdown(self,args):
    """
    TODO: refer to PyCubed website for further additions to this command
    Shutdown command, turns off satellite for specified period of time
    """
    if args == b'\x0b\xfdI\xec':
        self.debug('valid shutdown command received')
        # set shutdown NVM bit flag
        self.cubesat.f_shtdwn=True
        # stop all tasks
        for t in self.cubesat.scheduled_tasks:
            self.cubesat.scheduled_tasks[t].stop()
        self.cubesat.powermode('minimum')

        """
        Exercise for the user:
            Implement a means of waking up from shutdown
            See beep-sat guide for more details
            https://pycubed.org/resources
        """
        while True:
            time.sleep(100000)

def query(self,args):
    """
    sends valued queried over radio
    """
    self.debug('query: {}'.format(args))
    self.cubesat.radio1.send(data=str(eval(args)))

def exec_cmd(self,args):
    """
    TODO: refer to PyCubed website for further additions to this command
    executes command passed
    """
    self.debug('exec: {}'.format(args))
    exec(args)

def payload_start(self, args):
    """
    TODO
    Shutdown command, turns off satellite for specified period of time
    """
    # arg frequnecy will determine how often the payload will look for a transmission
    pass

def pl_cmd_arm(self, args):
    """
    command to payload arm
    """
    pass

def pl_cmd_photo(self, args):
    """
    command the payload to take a photo
    """
    pass

def pl_cmd_download_photo(self, args):
    """
    command the payload to send photo chunk
    """
    pass

def download_file(self, args):
    """
    download a file from the mainboard's SD card
    """
    pass

def upload_file(self, args):
    """
    upload a file to the mainboard's SD card
    """
    pass

def download_configs(self, args):
    """
    download a config for a specified task
    """
    pass

def upload_configs(self, args):
    """
    upload a config for a specified task
    """
    pass

def burst_test(self):
    """
    a test command to burst a photo down
    """
    # set flags and counters for the test_radio_file_transfer task to start
    self.cubesat.beacon=False
    self.cubesat.radio1_burst_flag = True
    self.cubesat.file_downlink_path = "/sd/cat.jpg"
    self.cubesat.brst_pkt_num = 0
    self.cubesat.scheduled_tasks['LoRa'].change_rate(100)


        