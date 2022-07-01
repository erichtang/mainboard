"""
foras_promineo_payload.py
====================================================================
Foras Promineo mission-specific payload library
only pertains to the payload, see foras_promineo_pib.py for things on the PIB.

* Authors C. Hillis
====================================================================

"""

class PAYLOAD():

    cmd_dispatch = {
        'noop' : b'f',
        'photo' : b'c',
        'move'  : b'm',
        'brst'  : b'b',
        'next_pkt' : b'n'
    }

    def __init__(self, satellite):
        """
        inherits satellite from pycubed.py
        """
        self.cubesat = satellite

        self.hardware = {
            'openMV' : False,
            #other payload devices ? openMV should handle it's own devices...
        }

        self.buf = bytearray(240) # 240 bytes of image data. last byte is always 
        self.buf_read = memoryview(self.buf)
        
        self.img_bst_flag = False # indication busrt mode is active
        self.buff_send_flag = False # indication that the lora_task.py can send the buffer data

        #init IO
        self.pwr_sw = self.cubesat.payload_pw_sw.value
        self.pwr_sw.value = True
        self.rst = self.cubesat.payload_rst
        self.rst.value = False
        self.servo_pwr_ctrl = self.cubesat.payload_servo_pwr_ctrl
        self.servo_pwr_ctrl.value = False

        # init openmv
        self.cubesat.uart2.write(self.cmd_dispatch['noop'])

        # recieve a byte ack from openmv
        ack = self.cubesat.uart2.read(nbytes=1)
        if ack is not None:
            self.hardware['openMV'] = True
        else:
            self.hardware['openMV'] = False
            self.pwr_sw.value = False
        
    

    