"""
Commands to and from the Foras Promineo Payload

1 byte command code, with args defined on a per-command basis. single commands are terminated with \r\n

"""

import time


rx = { # recieved codes from payload 
   b'\xff' : 'ACK',
   b'\xe5' : 'CMD_RESPONSE' 
}
tx = { # transmitted to payload
    'noop'          : b'\x00',
    'req_size'      : b'\xfe',
    'req_next_chunk': b'\xfd',
}

########### commands without arguments ###########

def noop(self):


    # send no-op

    self.debug('plcmds')
    # self.debug(time.time()*1000.0)

    write(self, 'noop')
    # look for a resonse
    self.cubesat.uart4.timeout = 6
    response = bytearray(3)
    
    response = self.cubesat.uart4.read(3)    
    # print(response)
    # response = self.cubesat.uart4.read(3) 
    # self.debug(time.time()*1000.0)    
    # x = self.cubesat.uart4.read(3)       
    # y = self.cubesat.uart4.read(3)  
    # print('asdfghjklasdhjklasdfghjklsdfghjkasdfghjklasdfghjklasdfghjkl')
    print(response)
    # self.debug(len(response))
    # print(x,y)

    # self.debug(response + 'response')
    # self.debug(response[0:1])
    # self.debug(rx[255])

    try:
        if rx[response[0:1]] == 'ACK':
            self.debug('ack')
            return True
        else:
            return False
    except Exception as e:
        return False

def testnoop(self):


    # send no-op

    self.debug('test')
    # self.debug(time.time()*1000.0)

    # look for a resonse
    self.cubesat.uart4.timeout = 0.01
    response = bytearray(3)
    
    response = self.cubesat.uart4.read(3)    
    # print(response)
    # response = self.cubesat.uart4.read(3) 
    # self.debug(time.time()*1000.0)    
    # x = self.cubesat.uart4.read(3)       
    # y = self.cubesat.uart4.read(3)  
    # print('asdfghjklasdhjklasdfghjklsdfghjkasdfghjklasdfghjklasdfghjkl')
    print(response)
    # self.debug(len(response))
    # print(x,y)

    # self.debug(response + 'response')
    # self.debug(response[0:1])
    # self.debug(rx[255])

    try:
        if rx[response[0:1]] == 'ACK':
            self.debug('ack')
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
    self.debug('reqchunk')
#CONVERT INT TO BYTES

    ind = chunk_i.to_bytes(3,'big')


    
    write(self, 'req_next_chunk', ind)
    # look for a resonse
    self.cubesat.uart4.timeout = 6
    response = self.cubesat.uart4.read(3)        #ERROR

    
    self.debug(response)
    


    len = int(response[1])

    self.debug(len)

    msg = self.cubesat.uart4.read(len)

    self.debug(msg)

    self.debug(response[0:1])

    try:
        if rx[response[0:1]] == 'CMD_RESPONSE':
            self.debug('chunk_resp')
            
            return msg
        else:
            return None
    except Exception as e:
        return False

def request_photo_size(self):
    write(self, 'req_size')
    # look for a resonse
    self.cubesat.uart4.timeout = 6

    self.debug('reqsize')

    

    response = self.cubesat.uart4.read(3)        #ERROR

    self.debug(response)

    len = int(response[1])
    self.debug(len)
    msg = int.from_bytes(self.cubesat.uart4.read(len), 'big')
    self.debug('msg')
    self.debug(msg)

    self.debug(response[0:1])
    try:
        if rx[response[0:1]] == 'CMD_RESPONSE':
            
            return msg
        else:
            return None
    except Exception as e:
        return False

    

################################################################

def wait4response(self):
    """
    helper functiopn to wait for a response
    """
    i = 0
    while True:
        #header = self.cubesat.uart4.read(3)
        #if header is not None
        #   return header
        if self.cubesat.uart4.in_waiting() >= 3:
            return self.cubesat.uart4.read(3)

        else:
            time.sleep(.01)
            i += 0
        if i >= 25:
            return False

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
    self.cubesat.uart4.write(msg)
    # self.debug(msg)