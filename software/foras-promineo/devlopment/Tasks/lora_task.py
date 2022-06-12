"""
LoRa radio operations 
modified code from beepsat_advanced code.

this task will be modified by execution of certian commands sent to the sat...

most of this code is unverified, but this is how i imagine it will execute...

* Author: Caden Hillis
Based upon beacon_task.py by Max Holliday
"""

from pdb import runctx
from Tasks.template_task import Task
import cdh
import foras_promineo_passcode as pc

class task(Task):
    #priority = 2
    #frequency = 1/30 # once every 30s
    name='LoRa'
    color = 'teal'

    schedule_later = False

    #default configuration settings
    d_cfg = {
        'priority' : 2,
        'frequnecy' : 1/30,
        'to' : 10,
        'dc_t' : 1
    }

    # our 4 byte codee to authorize commands
    # pass-code for DEMO PURPOSES ONLY
    super_secret_code = b'p\xba\xb8C'

    cmd_dispatch = {
        'no-op':        cdh.noop,
        'hreset':       cdh.hreset,
        'shutdown':     cdh.shutdown,
        'query':        cdh.query,
        'exec_cmd':     cdh.exec_cmd,
    }

    def __init__(self,satellite):
        self.cubesat = satellite
        # set our radiohead node ID so we can get ACKs
        self.cubesat.radio1.node = 0xFA # our ID
        self.cubesat.radio1.destination = 0xAB # target's ID

        self.cfg = self.d_cfg
        self.load_cfg(self.cfg, self.name)

        self.beacon = True
        self.connected = False
        self.dc_cnt = 0 # number of cycles without a response

    async def main_task(self):

        if self.beacon:
            #we we are not connected, send a beacon
            self.debug("Sending beacon")
            self.beacon()
            rx = self.listen()
            if rx is not None:
                self.rx_handler(rx)
            else:
                self.cubesat.radio1.sleep()

        # self.connected the GS wants to have tight comms and a lot of data exchange
        elif self.connected:
            if self.cubesat.payload.img_bst_flag: # if we are sending an image down 
                """
                maybe move this to a send_buff def?
                """
                if self.cubesat.payload.buff_send_flag: #if the buffer is ready to send
                    self.debug("Sending Packet:")
                    self.debug("{}".format(self.cubesat.payload.buf))
                    self.cubesat.radio1.send_fast(self.cubesat.payload.read_buf)
                    self.cubesat.payload.buff_send_flag = False
                    if self.cubesat.payload.read_buf[247:248] == b'0xffff': # if this is the end turn off img bst mode
                        self.cubesat.paylaod.img_bst = False
                    #clear the buffer
                    self.cubesat.payload.buf =  bytearray(248)
                    self.cubesat.payload.read_buf =  memoryview(self.cubesat.payload.buf)
            else:
                rx = self.listen() # what timeout should we use if it is connected?
                if rx is not None:
                    self.dc_cnt = 0
                    self.rx_handler(rx)
                else:
                    self.dc_count += 1
                    if self.dc_cnt >= self.dc_trig:
                        self.dc_cnt = 0
                        cdh.disconnect()
        
    def assemble_header(self):
        """
        tbr what the header will have. probably some flags ?
        """
        return bytearray(2)

    def beacon(self):
        #tries to initiate a downlink connection.
        # sends data and awaits a connect response from the GS.
        packet = self.assemble_packet(self) #TODO look into header instered on pycubed_rfm96 lib. maybe we can edit / minimize header length on our end.
        packet.append("Foras Promineo Cubesat Beacon")
        self.debug("Sending Packet: \n\t{}".format(packet))
        self.cubesat.radio1.send(packet, keep_listening=True,)
    
    async def listen(self, timeout):
        self.debug("Listening {}s for response (non-blocking)".format(timeout))
        heard_something = await self.cubesat.radio1.await_rx(timeout=timeout)
        if heard_something:
            # retrieve response
            response = self.cubesat.radio1.receive(keep_listening=True,with_ack=True)
            if response is not None:
                self.debug('msg: {}, RSSI: {}'.format(response,self.cubesat.radio1.last_rssi-137),2)
                self.cubesat.c_gs_resp+=1
                return response

    def rx_handler(self, rx):
        # TODO
        # Have this function check a transmitted flag that says if there are multiple commands or not.
        length = len(pc.top_secret_code)
        if rx[:length] == pc.top_secret_code:
            rx = rx[length-1:] #TODO check indexing
            while rx:
                if rx[:2] in self.cmd_dispatch: # looks for command
                    cmd = self.cmd_dispatch[rx[:2]]
                    args = None
                    if cdh.rx_cmd_arg_len[cmd] != 0: # if / if not args are passed
                        try: 
                            args = rx[2:2+cdh.rx_cmd_arg_len[cmd]]
                        except Exception as e:
                            self.debug("args decoding error".format(e), 2)
                    try: #try to execute
                        if args is None:
                            self.debug('running {} (no args)'.format(cmd), log=True)
                            self.cmd_dispatch[cdh.rx_cmd[cmd]](self)
                        else:
                            self.debug('running {} (with args)'.format(cmd), log=True)
                            self.debug('args: {})'.format(args), 2)
                            self.cmd_dispatch[cdh.rx_cmd[cmd]](self,args)
                    except Exception as e: #TODO implement a more concise error handler
                        self.debug('something went wrong: {}'.format(e))
                        error_packet = self.assemble_packet(self)
                        error_packet.append(cdh.tx_cmd['ERROR'])
                        self.cubesat.radio1.send(str(e).encode()) # THIS IS TEMPORARY, TODO CHANGE
                    try:
                        for b in range(2+cdh.rx_cmd_arg_len[cmd]):
                            rx.pop() #removing this command and it's args
                    except:
                        self.debug('command decode error: {}'.format(e))
                else:
                    self.debug("invalid command: {}".format(rx[:2])) 
                    #transmit invalid command
                    rx = None
        else:
            self.debug('bad passcode recieved: {}'.format(rx[:length]))
            
    def error_handler(self):
        #records packet IDs of missing packets and requests them? IDK
        #TBR THIS WILL PROBABLY HAVE TO BE MUCH MORE SOPHISTICATED?
        error_packet = self.assemble_packet(self)
        error_packet.append(cdh.tx_cmd['ERROR'])
        self.cubesat.radio1.send(error_packet) # THIS IS TEMPORARY
