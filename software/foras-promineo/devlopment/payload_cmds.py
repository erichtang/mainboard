"""
Commands to and from the Foras Promineo Payload

1 byte command code, with args defined on a per-command basis. single commands are terminated with \r\n

"""

import time

rx = { # recieved codes from payload 
   b'\xff' : 'ACK',
   b'\x01' : 'size'
}
tx = { # transmitted to payload
    'noop'          : b'\x00',
    'req_size'      : b'\xfe',
    'req_next_chunk': b'\xfd',
}

########### commands without arguments ###########

def noop(self):


    # send no-op
    write(self, 'noop')
    # look for a resonse
    self.cubesat.uart2.timeout = 0.01
    response = self.cubesat.uart2.read(3)        #ERROR

    try:
        if rx[response[0]] == 'ACK':
            
            return True
        else:
            return False
    except Exception as e:
        return False

def hreset(self):
    pass

def sreset(self):
    pass

def read_servo_ctrl_status(self, args):
    pass

def read_ilim(self, args):
    pass

def read_servo_pwm(self, args):
    pass

def read_clr_status(self, args):
    pass

def read_stepper_pwr_status(self, args):
    pass

def read_stepper_ctrl(self, args):
    pass

########### commands with arguments ###########

def query(self, args):
    pass

def exec_cmd(self, args):
    pass

def set_servo_ctrl(self, args):
    pass

def set_ilim(self, args):
    pass

def set_servo_pwm(self, args):
    pass

def set_clr_ctrl(self, args):
    pass
        
def set_stepper_pwr_ctrl(self, args):
    pass

def set_stepper_ctrl(self, args):
    pass

def take_photo(self, args):
    pass

def request_photo_chunk(self, chunk_i):

#CONVERT INT TO BYTES

    ind = chunk_i.to_bytes(2,'big')

    write(self, 'req_next_chunk', ind)
    # look for a resonse
    self.cubesat.uart2.timeout = 0.01
    response = self.cubesat.uart2.read(3)        #ERROR
    len = int(response[1])
    msg = int(self.cubesat.uart2.read(len))
    try:
        if rx[response[0]] == 'cmd_response':
            
            return msg
        else:
            return None
    except Exception as e:
        return False

def request_photo_size(self):
    write(self, 'req_size')
    # look for a resonse
    self.cubesat.uart2.timeout = 0.01
    response = self.cubesat.uart2.read(3)        #ERROR
    len = int(response[1])
    msg = int(self.cubesat.uart2.read(len))
    try:
        if rx[response[0]] == 'size':
            
            return msg
        else:
            return None
    except Exception as e:
        return False

################################################################

def write(self, cmd, data=None):
    """
    helper function to write to the payload.
    """
    #get length
    if data is None:
        length = 0
    else:
        length = len(data)
    
    #assemble header
    msg = bytearray(3+length)
    # self.debug(tx[cmd][0])
    msg[0] = tx[cmd][0]
    msg[1] = length
    msg[2] = 0
    if length > 0:
        msg[3:] = data
    self.cubesat.uart2.write(msg)