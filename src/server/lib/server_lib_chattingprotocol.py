# 
# Server side code
#
# Chatting (N:M) Service Protocol
#
# ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_server.py
#

import struct
import logging
import binascii

from aioquic.asyncio import QuicConnectionProtocol
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionIdIssued, ConnectionTerminated

#
# configuration functions for server.py
#

def get_protocol_class():
    return ChattingServerProtocol

def get_protocol_name():
    return 'Chatting over QUIC' 

def get_protocol_alpn():
    return 'coq'

def save_quic_server_pointer(ptr):
    ChattingServerProtocol.quic_server_pointer = ptr

#
# simple loopback service protocol code @ here 
#

class ChattingServerProtocol(QuicConnectionProtocol): 

    quic_server_pointer  = None  # static variable : pointer to QUIC server
    quic_server_sessions = set() # static variable : sessions in QUIC server

    @property
    def q_ptr(self):
        return ChattingServerProtocol.quic_server_pointer

    @property
    def q_ses(self):
        return ChattingServerProtocol.quic_server_sessions

    def quic_event_received(self, event: QuicEvent):

        if isinstance(event, StreamDataReceived):
            
            # unpack query
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            data = event.data[2 : 2 + length]
            
            # do something
            logging.info('[strm:{}] {}'.format(event.stream_id, data))

            # pack query result
            data = struct.pack("!H", len(data)) + data

            # send answer
            self.broadcast(data)

        elif isinstance(event, ConnectionIdIssued):

            if self._quic.host_cid not in self.q_ses:
                self.q_ses.add(self._quic.host_cid)
                logging.info('session added: {}'.format(binascii.hexlify(self._quic.host_cid)))

        elif isinstance(event, ConnectionTerminated):

            if self._quic.host_cid in self.q_ses:
                self.q_ses.remove(self._quic.host_cid)
                logging.info('session removed: {}'.format(binascii.hexlify(self._quic.host_cid)))

    def broadcast(self, data):

        for cid in self.q_ses:
            id = self.q_ptr._protocols[cid]._quic.get_next_available_stream_id()
            self.q_ptr._protocols[cid]._quic.send_stream_data(id, data, end_stream=True)
            self.q_ptr._protocols[cid].transmit()

#
# QUIC Evnets ?
#
# ref: https://aioquic.readthedocs.io/en/latest/quic.html#module-aioquic.quic.events 
# ref: https://github.com/aiortc/aioquic/blob/main/src/aioquic/quic/events.py
# 

#
# pack ?
#
# struct.pack() converts between Python values and C structs represented as Python bytes objects
# ref: https://docs.python.org/3/library/struct.html 
#
# ! means network (= big-endian)
# ref: https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment
#
# H means unsigned short in C
# ref: https://docs.python.org/3/library/struct.html#format-characters 
#