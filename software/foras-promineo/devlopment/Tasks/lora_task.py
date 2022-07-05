"""
TODO -- lora radio conops and packet structure are still under devlopment. this will probably change.
LoRa radio operations for beacon, connected, and payload satellite states.

Functionalities:
    Beacon Mode: LoRa transmits a repeating message and listens for responses.
        beacon tx --> rx command --> ex cmd
    Burst Mode: LoRa transmits data in a quick succession.
        tx chunk 0 --> tx chunk 1 --> tx chunk 2 ......
    Connected Mode: LoRa listens more frequenctly to recieve successive commands from the ground station
        rx command --> ex cmd --> rx cmd --> ex cmd......

Implementation status:
    Header -- still a work in progress, but workable for now
    Beacon -- Single packet tx and rx have been verified.
    Burst -- working on verifying burst with test_radio_file_transfer.py
    Connected -- WIP

Notes:
    I have some flags defined in pycubed.py for burst mode transmission, thouse should probably go and live somewhere else eventually.

Wishlist:
    multiple packets flag / counter for recieveing args for a command longer than 242 bytes
    implementing a "command queue" task that queues radio commands and their args so that the radio can just focus on listening.
    file burst uplink similar to burst downlink

* Author: Caden Hillis
Based upon beacon_task.py by Max Holliday from beepsat_advanced devlopment branch.
"""

import time
from Tasks.template_task import Task
import cdh
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
        'dc_t' : 1,
        'c_to' : .1 # connected timeout
    }

    cmd_dispatch = {
        'no-op':        cdh.noop,
        'hreset':       cdh.hreset,
        'shutdown':     cdh.shutdown,
        'query':        cdh.query,
        'exec_cmd':     cdh.exec_cmd,
        'burst_test':   cdh.burst_test,
    }

    def __init__(self,satellite):
        self.cubesat = satellite
        # set our radiohead node ID so we can get ACKs
        #self.cubesat.radio1.node = 0xFA # our ID
        #self.cubesat.radio1.destination = 0xAB # target's ID

        self.cfg = self.d_cfg
        self.load_cfg(self.cfg, self.name)

        #self.beacon = True
        self.connected = False
        self.dc_cnt = 0 # number of cycles without a response

    async def main_task(self):

        if self.cubesat.beacon:
            #we we are not connected, send a beacon
            self.tx_beacon()
            rx = await self.listen(self.cfg['b_to'])
            if rx is not None:
                self.debug("Heard Something: ")
                self.debug("{}".format(rx),2)
                self.rx_handler(rx)

        # burst mode has priority over connected mode
        # if we are bursting data and the buffer is ready
        elif self.cubesat.radio1_burst_flag and self.cubesat.send_buff_ready_flag:

            if self.cubesat.brst_pkt_num == 0: #if this is the first packet
                # assemble burst start packet
                brst_start_tx = self.assemble_header(multiple_packets=True)
                brst_start_tx += cdh.tx['BRST_ST'] 
                # send burst start command
                self.debug("Transmitting Burst Start: {}".format(brst_start_tx))
                self.cubesat.radio1.send(brst_start_tx, keep_listening=False)
                # record time of start
                self.cubesat.burst_st_time = time.monotonic()

            # now send the buffer
            # add the header to the send buffer
            self.cubesat.send_buff[:10] = self.assemble_header(multiple_packets=True, packet_number=self.cubesat.brst_pkt_num+1, outof = self.cubesat.brst_pkt_tot+2)
            self.cubesat.send_buff_tx_len += 10 # increment send buffer length by header length

            # send packet
            self.debug("Sending Burst Packet {}".format(self.cubesat.brst_pkt_num))
            #self.debug('{}'.format(bytearray(self.cubesat.send_buff[:self.cubesat.send_buff_tx_len])))

            if not self.cubesat.radio1.send(self.cubesat.send_buff[:self.cubesat.send_buff_tx_len], keep_listening=False):
                self.debug("Burst Packet Tx FAIL")
            # if that was the last packet
            if self.cubesat.brst_pkt_num == self.cubesat.brst_pkt_tot - 1: 
                time_elapsed = time.monotonic() - self.cubesat.burst_st_time
                # assemble burst end packet
                brst_end_tx = self.assemble_header(multiple_packets=True, packet_number=self.cubesat.brst_pkt_tot+2, outof=self.cubesat.brst_pkt_tot+2)
                brst_end_tx += cdh.tx['BRST_END'] 
                # send burst end command
                self.debug("Transmitting Burst End: {}".format(brst_end_tx))
                self.cubesat.radio1.send(brst_end_tx)
                #turn the bursting off
                self.cubesat.send_buff_ready_flag = False
                self.cubesat.radio1_burst_flag = False
                self.cubesat.beacon = True
                self.cubesat.scheduled_tasks['LoRa'].change_rate(self.cfg['frequency'])
                self.debug("Burst Done. Transmitted {} bytes in {} seconds".format(self.cubesat.file_downlink_size, time_elapsed))
            
            else:  # reset flag and increment packet counter for getter task to get next set of data         
                self.cubesat.brst_pkt_num += 1
                self.cubesat.send_buff_ready_flag = False

        # self.connected the GS wants to have tight comms and a lot of data exchange
        elif self.connected:
            rx = self.listen(self.cfg['c_to']) # what timeout should we use if it is connected?
            if rx is not None:
                self.dc_cnt = 0
                self.rx_handler(rx)
            else:
                self.dc_count += 1
                if self.dc_cnt >= self.config['dc_t']:
                    self.dc_cnt = 0
                    cdh.disconnect()
        
    def assemble_header(self, listen_again = False, multiple_packets = False, packet_number = 0, outof = 0):
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
        #header[4] |= (multiple_cmds & 0x4) #TODO add more flags?
        header[5] = 0
        # multiple packets
        if not multiple_packets:
            header[6] = (packet_number >> 8) & 0xff
            header[7] = (packet_number ) & 0xff
            header[8] = (outof >> 8) & 0xff
            header[9] = outof & 0xff
        else:
            pass
        return header

    def tx_beacon(self):
        # tries to initiate a downlink connection.
        # sends data and awaits a connect response from the GS.
        packet = self.assemble_header()
        packet += cdh.tx['BEACON'] 
        # figure out what telemetry we want to send via beacon...
        self.debug("Sending Beacon:")
        self.debug("{}".format(packet), level=2)
        if not self.cubesat.radio1.send(bytearray(packet), keep_listening=True):
            self.debug("tx error")
    
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
            h_flags = rx[4:6]
            h_no = rx[6:8]
            h_total = rx[8:10]

            cmd = rx[10:12]
            if cmd in cdh.rx: # looks for command
                cmd = cdh.rx[cmd] # re-assigning cmd to be key for cdh dict
            else:
                self.error_handler("invalid command: {}".format(cmd))
                return 
            args = None
            """
            Re-write next section to be compatable with new change caden ()n mkade
            """
            try: 
                args = rx[12:]
            except Exception as e:
                self.error_handler("args decoding error: {}".format(e))
            try: #try to execute
                if len(args) == 0:
                    self.debug('running {} (no args)'.format(cmd), log=True)
                    self.cmd_dispatch[cmd](self)
                else:
                    self.debug('running {} (with args)'.format(cmd), log=True)
                    self.debug('args: {})'.format(args), 2)
                    self.cmd_dispatch[cmd](self,args)
            except Exception as e:
                self.error_handler("cmd execution error: {}".format(e))

            # if listen again flag
            if rx[4] & 0x3 == 0x3:

                
                # multiple command / multiple packet execution
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
        error_packet += (cdh.tx['ERROR'])
        error_packet += e
        self.cubesat.radio1.send(error_packet, keep_listening=True) # THIS IS TEMPORARY, TODO CHANGE
        # IF MULTIPLE PACKETS ARE SENT this needs to be SENT AFTER ALL PACKETS HAVE BEEN RX'd

