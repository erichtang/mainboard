"""
TODO -- lora radio conops and packet structure are still under devlopment. this will probably change.
LoRa radio operations for beacon, connected, and payload satellite states.

this task will be modified by execution of certian commands sent to the sat...
TODO:
    single packet single cmd rx during beacon is verified
    multiple packet, multiple cmd, connected mode, and payload mode are not done or verified....

* Author: Caden Hillis
Based upon beacon_task.py by Max Holliday from beepsat_advanced devlopment branch.
"""

from Tasks.template_task import Task
import cdh
import passcode as pc

class task(Task):
    #priority = 2
    #frequency = 1/30 # once every 30s
    name='LoRa'
    color = 'teal'

    schedule_later = False

    #default configuration settings
    d_cfg = {
        'priority' : 2,
        'frequency' : 1/10,
        'b_to' : 10, # beacon timeout
        'dc_t' : 1,
        'c_to' : .1 # connected timeout
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
        #self.cubesat.radio1.node = 0xFA # our ID
        #self.cubesat.radio1.destination = 0xAB # target's ID

        self.cfg = self.d_cfg
        self.load_cfg(self.cfg, self.name)

        self.beacon = True
        self.connected = False
        self.dc_cnt = 0 # number of cycles without a response

    async def main_task(self):

        if self.beacon:
            #we we are not connected, send a beacon
            #self.debug("Sending beacon")
            self.tx_beacon()
            rx = await self.listen(self.cfg['b_to'])
            if rx is not None:
                self.debug("Heard Something: ")
                self.debug("{}".format(rx),2)
                try:
                    self.rx_handler(rx)
                except:
                    self.debug("rx problem remove me later")
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
                rx = self.listen(self.cfg['c_to']) # what timeout should we use if it is connected?
                if rx is not None:
                    self.dc_cnt = 0
                    self.rx_handler(rx)
                else:
                    self.dc_count += 1
                    if self.dc_cnt >= self.dc_trig:
                        self.dc_cnt = 0
                        cdh.disconnect()
        
    def assemble_header(self, listen_again = False, multiple_packets = False, multiple_cmds = False, packet_number = 0, outof = 0):
        """
        adds passcode, flags, and packet counters to packet. 
        10 bytes total...
        passcode:(4 bytes for now)
             gets from pc.top_secret_code
        flags: (2 bytes for now) 
            b0 : tells reciever to listen again before no-op CMD. default : false
            b1 : multiple packet flag
            b2 : multiple cmd flag
            b3 :
            b4 :
            b5 :
            b6 : 1
            b7 : 0
            --
            b8 :
            ...
            b14 : 1
            b15 : 0
        packet counter: (4 bytes for now)
            not really implemented yet, 
            something doesn't like pairs of unicode "\x00"'s so they're avoided...
        """
        header = bytearray(10)
        #code
        header[0] = pc.top_secret_code[0]
        header[1] = pc.top_secret_code[1]
        header[2] = pc.top_secret_code[2]
        header[3] = pc.top_secret_code[3]
        # flags
        header[4] = 0
        header[4] |= (listen_again & 0x1) 
        header[4] |= (multiple_packets & 0x2) 
        header[4] |= (multiple_cmds & 0x4) #TODO add more flags?
        header[5] = 0
        # multiple packets
        if not multiple_packets:
            header[6:10] = bytearray("beef".encode('utf-8'))
        else:
            pass
        print(header)
        return header

    def tx_beacon(self):
        #tries to initiate a downlink connection.
        # sends data and awaits a connect response from the GS.
        packet = self.assemble_header()
        packet += "Foras Promineo Cubesat Beacon Test Packet" # TODO Change for flight
        self.debug("Sending Packet:")
        self.debug("{}".format(packet), level=2)
        if not self.cubesat.radio1.send(bytearray(packet), keep_listening=True):
            self.debug("tx error")
    
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
        code = rx[:4]
        if code == pc.top_secret_code:
            h_flags = rx[4:6]
            h_no = rx[6:8]
            h_total = rx[8:10]
            if h_flags[0] & 0x4 == 0: #checking multiple cmd's header... TODO : maybe implement a function to handle the header and guide execution after?
                # single command execution
                cmd = rx[10:12]
                if cmd in cdh.cmd: # looks for command
                    cmd = cdh.cmd[cmd] # re-assigning cmd to be key for cdh dict
                else:
                    self.error_handler("invalid command: {}".format(cmd)) 
                args = None
                if cdh.arg_len[cmd] != 0: # if / if not args are passed
                    try: 
                        args = rx[12:12+cdh.arg_len[cmd]]
                    except Exception as e:
                        self.error_handler("args decoding error: {}".format(e))
                try: #try to execute
                    if args is None:
                        self.debug('running {} (no args)'.format(cmd), log=True)
                        self.cmd_dispatch[cmd](self)
                    else:
                        self.debug('running {} (with args)'.format(cmd), log=True)
                        self.debug('args: {})'.format(args), 2)
                        self.cmd_dispatch[cmd](self,args)
                except Exception as e:
                    self.error_handler("cmd execution error: {}".format(e))
            else:
                # multiple command execution
                #not implemented yet....
                """
                try:
                    for b in range(2+cdh.rx_cmd_arg_len[cmd]):
                        rx.pop() #removing this command and it's args
                except:
                    self.debug('command decode error: {}'.format(e))
                """
                pass
            # listen again flag handler
                # implement handling for multiple packet tx's -- probably a part of listen again?
        else:
            self.error_handler('bad passcode recieved: {}'.format(code))
            
    def error_handler(self, e):
        #records packet IDs of missing packets and requests them? IDK
        #TBR THIS WILL PROBABLY HAVE TO BE MUCH MORE SOPHISTICATED?
        self.debug(e)
        error_packet = self.assemble_header(self)
        error_packet += (cdh.resp['ERROR'])
        error_packet += e
        self.cubesat.radio1.send(error_packet, keep_listening=True) # THIS IS TEMPORARY, TODO CHANGE
        # IF MULTIPLE PACKETS ARE SENT this needs to be SENT AFTER ALL PACKETS HAVE BEEN RX'd

