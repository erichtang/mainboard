import time

#generic pycubed commands, not edited.
cmd = {
    b'\x8eb': 'no-op',
    b'\xd4\x9f': 'hreset',
    b'\x12\x06': 'shutdown',
    b'8\x93': 'query',
    b'\x96\xa2': 'exec_cmd',
}

tx_cmd = { #commands transmitted
    
}

rx_cmd = { #commands recieved
    'connect' : b'\xf0'
}

rx_cmd_arg_len = { #number of bytes of args after each rx command. useful for multiple commands in one packet.
    'connect' : 0
}

########### commands without arguments ###########
def noop(self):
    self.debug('no-op')
    pass

def hreset(self):
    self.debug('Resetting')
    try:
        self.cubesat.radio1.send(data=b'resetting')
        self.cubesat.micro.on_next_reset(self.cubesat.micro.RunMode.NORMAL)
        self.cubesat.micro.reset()
    except:
        pass

def connect(self):
    self.connected = True
    # do a settings load?

def disconnect(self):
    self.connected = False
    self.cubesat.radio1.sleep()
    # change other task settings

########### commands with arguments ###########

def shutdown(self,args):
    # make shutdown require yet another pass-code
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
    self.debug('query: {}'.format(args))
    self.cubesat.radio1.send(data=str(eval(args)))

def exec_cmd(self,args):
    self.debug('exec: {}'.format(args))
    exec(args)

def payload_start(self, args):
    # arg frequnecy will determine how often the payload will look for a transmission
    pass

def img_bst(self, args):
    self.cubesat.payload.img_bst_flag = True
    self.cubesat.uart2.write(self.cubesat.payload.cmd_dispatch['brst'])
    self.cubesat.radio1.idle() #stop radio from listening for other packets
    pass




        