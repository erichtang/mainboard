"""
TODO -- lora radio conops and packet structure are still under devlopment. this will probably change.
LoRa radio operations for beacon, and connected modes.
    NOTE burst transfer downlink is handled in burst_transfer_task.py any cmd that initiates a radio burst downlink should stop() this task.

Functionalities:
    Beacon Mode: LoRa transmits a repeating message and listens for responses.
        beacon tx --> rx command --> ex cmd
    Connehcted Mode: LoRa listens more frequenctly to recieve successive commands from te ground station
        rx command --> ex cmd --> rx cmd --> ex cmd......

Implementation status:
    Header -- still a work in progress, but workable for now
    Beacon -- Single packet tx and rx have been verified.
    Burst -- see burst_transfer_task.py
    Connected -- WIP

Notes:
    I have some flags defined in pycubed.py for burst mode transmission, thouse should probably go and live somewhere else eventually.

    I do not forsee a good usage case for radio commands and/or message lengths longer than a single packet:
        if such a large data transfer is required, one would probably want to use the burst transfer task with a LoRa source for such large transactions.
        It just adds too much handling complexity for a concise and succient radio implementation.....

Wishlist:
    multiple packets flag / counter for recieveing args for a command longer than 242 bytes
    implementing a "command queue" task that queues radio commands and their args so that the radio can just focus on listening.
    file burst uplink similar to burst downlink

* Author: Caden Hillis
Based upon beacon_task.py by Max Holliday from beepsat_advanced devlopment branch.
"""

import time
from Tasks.template_task import Task
import lora_cmds
import passcode as pc

class task(Task):
    name='LoRa'
    color = 'teal'

    schedule_later = False

    #default configuration settings
    d_cfg = {
        'priority' : 2,
        'frequency' : 1/10,
        'b_to' : 10, # beacon timeout
        'dc_trig' : 1, # disconnect trigger
        'c_to' : .1 # connected timeout
    }

    cmd_dispatch = {
        'no-op':        lora_cmds.noop,
        'hreset':       lora_cmds.hreset,
        'shutdown':     lora_cmds.shutdown,
        'query':        lora_cmds.query,
        'exec_cmd':     lora_cmds.exec_cmd,
        'burst_test':   lora_cmds.burst_test,
        # add more !!!!
    }

    def __init__(self, cubesat):
        super().__init__(cubesat)

        self.beacon_f = True
        self.connected_f = False
        self.dc_c = 0 # number of cycles without a response

    async def main_task(self):

        if self.beacon_f:
            self.tx_beacon()
            rx = await self.listen(self.cfg['b_to'])
            if rx is not None:
                self.debug("Heard Something: ")
                self.debug("{}".format(rx),2)
                self.rx_handler(rx)

        # self.connected_f the GS wants to have tight comms with a quick data exchange
        elif self.connected_f:
            rx = self.listen(self.cfg['c_to']) # what timeout should we use if it is connected?
            if rx is not None:
                self.dc_c = 0
                self.rx_handler(rx)
            else:
                self.dc_c += 1
                if self.dc_c >= self.config['dc_trig']:
                    self.dc_c = 0
                    lora_cmds.disconnect()
        
    def assemble_header(self, listen_again = False, cmd = b'\x00\x00', length = 0, packet_number = 0, outof = 0):
        """
        adds passcode, flags, and packet counters to packet. 
        12 bytes total...
        passcode:(4 bytes for now)
             gets from pc.top_secret_code
             look into a more secure and not very processor intensive security method
        flags: (1 byte for now) 
            b0 : tells GS reciever to listen again for another transmission. (Usefule for a low-speed medium-data cmd response that isn't large enough for a burst transfer of data)
            b1 :
            b2 :
            b3 :
            b4 :
            b5 :
            b6 : 1
            b7 : 0
        packet length: (1 byte) : number of bytes AFTER the header
        packet counter: (4 bytes for now)
            this isn't really final so be prepared for it to change..........
        cmd code: (2 bytes) : 2 byte command code corresponding to a key in lora_cmds.rx dict
        """
        header = bytearray(12)
        #code
        header[0] = pc.top_secret_code[0]
        header[1] = pc.top_secret_code[1]
        header[2] = pc.top_secret_code[2]
        header[3] = pc.top_secret_code[3]
        # flags
        # TODO clean up flags, i dont really like these.......,.
        header[4] = 0 | (listen_again & 0x1) 
        header[5] = (length) & 0xff
        # packet counts -- these are all usually zero -- 
            # TODO maybe only have these if a certian flag is set?
        header[6] = (packet_number >> 8) & 0xff
        header[7] = (packet_number) & 0xff
        header[8] = (outof >> 8) & 0xff
        header[9] = outof & 0xff
        header[10:12] = lora_cmds.tx[cmd]
        return header

    def tx_beacon(self):
        # tries to initiate a downlink connection.
        # sends data and awaits a connect response from the GS.
        packet = self.assemble_header(cmd='BEACON')
        # figure out what telemetry we want to send via beacon...
        self.debug("Sending Beacon:")
        self.debug("{}".format(packet), level=2)
        if not self.cubesat.radio1.send(bytearray(packet), keep_listening=True):
            self.debug("tx error") # this should raise an exception for error handling!
    
    async def listen(self, timeout):
        self.debug("Listening {}s for response (non-blocking)".format(timeout))
        heard_something = await self.cubesat.radio1.await_rx(timeout=timeout)
        if heard_something:
            # retrieve response
            response = self.cubesat.radio1.receive(keep_listening=True,with_ack=True, with_header=False, timeout=timeout)
            if response is not None:
                self.debug('msg: {}, RSSI: {}'.format(response,self.cubesat.radio1.last_rssi-137),2)
                self.cubesat.c_gs_resp+=1
                return response

    def rx_handler(self, rx):
        code = rx[:4]
        #code has to be right if rx will handle
        if code == pc.top_secret_code:
            
            # ignoring flags for now...

            cmd = rx[10:12]
            if cmd in lora_cmds.rx: # looks for command
                cmd = lora_cmds.rx[cmd] # re-assigning cmd to be key for cdh dict
            else:
                self.error_handler("invalid command: {}".format(cmd)) # do better error handling.....
                return 

            try:
                # if there are arguments passed with the command
                if rx[5] != b'\x00':
                    # try to execute command wintout args
                    self.debug('running {} (no args)'.format(cmd), log=True)
                    self.cmd_dispatch[cmd](self)
                else:
                    # assign args
                    args = rx[12:]
                    # try to execute with args
                    self.debug('running {} (with args)'.format(cmd), log=True)
                    self.debug('args: {})'.format(args), 2)
                    self.cmd_dispatch[cmd](self, args)
            except Exception as e:
                self.error_handler("cmd execution error: {}".format(e))
        else:
            self.error_handler('bad passcode recieved: {}'.format(code))
            
    def error_handler(self, e):
        #records packet IDs of missing packets and requests them? IDK
        #TBR THIS WILL PROBABLY HAVE TO BE MUCH MORE SOPHISTICATED?
        self.debug(e)
        error_packet = self.assemble_header(self)
        error_packet += (lora_cmds.tx['ERROR'])
        error_packet += e
        self.cubesat.radio1.send(error_packet, keep_listening=True) # THIS IS TEMPORARY, TODO CHANGE
        # IF MULTIPLE PACKETS ARE SENT this needs to be SENT AFTER ALL PACKETS HAVE BEEN RX'd

