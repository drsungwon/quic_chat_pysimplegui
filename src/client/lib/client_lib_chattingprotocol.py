# 
# Client side code
#
# PySimple GUI Chatting Service Protocol
#
# ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_client.py
#

import asyncio
import struct
import logging

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived

#
# pysimple gui client related packages & functions
#

import PySimpleGUI as sg
from datetime import datetime

def create_gui_layout(chat_info):

    # left plane : chatting messages

    title = 'Started: ' + datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    l_1_a = sg.Output(size=(50, 20))
    l_2_t = sg.Text(title, size=(40, 1))

    grp_l = sg.Frame(' Chatting Messages ', [[l_1_a], [l_2_t]])

    # right plane : menus

    r_1_t = sg.Text('Chatting ID', size=(10, 1))
    r_1_i = sg.In(size=(20,1), key='-CHATTINGID-')
    r_2_t = sg.Text('Server', size=(10, 1))
    r_2_s = sg.Text(chat_info.server_ip + ':' + str(chat_info.server_port), size=(20, 1), relief='sunken')
    r_3_t = sg.Text('Client (Me)', size=(10, 1))
    r_3_s = sg.Text('', size=(20,1), key='-CLIENTINFO-', relief='sunken')
    r_4_t = sg.Text('Session', size=(10, 1))
    r_4_s = sg.Text('CONNECTED', size=(20,1), key='-CONNSTATUS-', relief='sunken')   

    r_6_t = sg.Text('Type & SEND to transmit', size=(30, 1))
    r_7_m = sg.Multiline(size=(30, 4), font=('Consolas', 13), key='-QUERY-', do_not_clear=False)
    r_8_b = sg.Button('SEND', size=(31, 1), button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True)
            
    r_9_b = sg.Button('EXIT', size=(31, 1), button_color=(sg.YELLOWS[0], sg.GREENS[0]))

    f_r_1 = sg.Frame(' Service Information ',[[r_1_t, r_1_i], [r_2_t, r_2_s], [r_3_t, r_3_s], [r_4_t, r_4_s]])
    f_r_2 = sg.Frame(' Chatting ',[[r_6_t],[r_7_m],[r_8_b]])
    f_r_3 = sg.Frame(' Service Termination ', [[r_9_b]])

    grp_r = sg.Column([[f_r_1], [f_r_2], [f_r_3]])

    # complete layout

    final_layout = [ grp_l, grp_r ]
    final_layout = [ sg.vtop( final_layout ) ]

    return final_layout

class Chatting_Service_Info:
    def __init__(self, server_ip='127.0.0.1', server_port=8053):
        self.server_ip = server_ip
        self.server_port = server_port
        self.id = ''
        self.delimeter = '|'

def print_info(msg):
    print(msg)

def encode_chat(chat_info, msg):
    message = chat_info.id + chat_info.delimeter + msg
    return message

def decode_chat(chat_info, msg):
    id, text = msg.decode('utf-8').split(chat_info.delimeter)
    return id, text

#
# configuration functions for client.py
#

def get_protocol_class():
    return ChattingClientProtocol

def get_protocol_name():
    return 'Chatting over QUIC' 

def get_protocol_alpn():
    return 'coq'

#
# simple loopback service protocol code @ here 
#

class ChattingClientProtocol(QuicConnectionProtocol):

    async def activate_protocol(self) -> None:
        '''
        Callback which is invoked by the client.py when a client program is executed
        '''

        # activate pysimplegui process
        self.chat_info = Chatting_Service_Info()
        self.window = sg.Window('QUIC Chatting Program Ver.1', 
            create_gui_layout(self.chat_info), font=('Consolas', 13), use_default_focus=False)
        
        # chatting forever
        while True:          

            # async wait for pysimplegui event
            # ref: https://gist.github.com/ultrafunkamsterdam/f840d48ba3451121b7197e7cde7ac303
            await asyncio.sleep(0.01)   
            event, values = self.window.read(0)

            # SEND button pressed
            if event == 'SEND':

                # configure chatting client identifier
                if self.chat_info.id == '':
                    id = values['-CHATTINGID-']
                    if len(id) == 0:
                        print_info('[INFO] Chatting ID required: {} ({})'.format(self.chat_info.id, len(id)))
                    else:
                        self.chat_info.id = id
                        print_info('[INFO] Chatting ID configured: {} ({})'.format(self.chat_info.id, len(id)))

                # if identifier is configured, send message to server
                if self.chat_info.id != '':
                    send_text = values['-QUERY-'].rstrip()
                    await self.send_loopback_msg(str(encode_chat(self.chat_info, send_text)))
                    print_info('[SEND] {}'.format(send_text))

            # EXIT, DISCONNECT, X buttons pressed
            elif event in (sg.WIN_CLOSED, 'EXIT', 'DISCONNECT'): 
                break

        # terminate pysimplegui and exit
        self.window.close()

    async def send_loopback_msg(self, msg: str) -> None:

        # make message to send
        data = bytes(msg, encoding='utf8')
        data = struct.pack("!H", len(data)) + data

        # send message 
        self.stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(self.stream_id, data, end_stream=True)
        self.transmit()
        logging.info("send_loopback_msg(): {} sent".format(msg))

    def quic_event_received(self, event: QuicEvent) -> None:

        if isinstance(event, StreamDataReceived):
            # parse answer
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            msg = event.data[2 : 2 + length]

            # decode chatting message and display over pysimplegui
            id, msg = decode_chat(self.chat_info, msg)
            if id != self.chat_info.id:
                print_info("[RECV] {} (@{})".format(msg, id))
                logging.info("quic_event_received(): {}".format(msg))
            else:
                logging.info("quic_event_received(): {} [but ignored]".format(msg))

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

