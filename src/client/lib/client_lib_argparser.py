#
# Client side code
#
# Ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_client.py
# Ref: https://aioquic.readthedocs.io/en/latest/asyncio.html
# Ref: https://aioquic.readthedocs.io/en/latest/quic.html#module-aioquic.quic.configuration
#

import argparse
import pickle
import ssl
import logging

from aioquic.quic.configuration import QuicConfiguration

def get_args_parser(protocol_name: str):
    # protocol_name example : 'DNS over QUIC'

    parser = argparse.ArgumentParser(description=protocol_name)

    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="The remote peer's host name or IP address",
    )

    parser.add_argument(
        "--port", 
        type=int, 
        default=853, 
        help="The remote peer's port number"
    )

    parser.add_argument(
        "-k",
        "--insecure",
        action="store_true",
        help="do not validate server certificate",
    )

    parser.add_argument(
        "--ca-certs", 
        type=str, 
        help="load CA certificates from the specified file"
    )
    
    parser.add_argument(
        "-q",
        "--quic-log",
        type=str,
        help="log QUIC events to QLOG files in the specified directory",
    )

    parser.add_argument(
        "-l",
        "--secrets-log",
        type=str,
        help="log secrets to a file, for use with Wireshark",
    )

    parser.add_argument(
        "-s",
        "--session-ticket",
        type=str,
        help="read and write session ticket from the specified file",
    )

    parser.add_argument(
        "-v", 
        "--verbose", 
        action="store_true", 
        help="increase logging verbosity"
    )

    return parser.parse_args()

def set_quic_configuration(quic_conf: QuicConfiguration, args):
    
    if args.ca_certs:
        quic_conf.load_verify_locations(args.ca_certs)
    
    if args.insecure:
        quic_conf.verify_mode = ssl.CERT_NONE
    
    if args.quic_log:
        quic_conf.quic_logger = quic_conf(args.quic_log)
    
    if args.secrets_log:
        quic_conf.secrets_log_file = open(args.secrets_log, "a")
    
    if args.session_ticket:
        try:
            with open(args.session_ticket, "rb") as fp:
                quic_conf.session_ticket = pickle.load(fp)
        except FileNotFoundError:
            logging.debug(f"Unable to read {args.session_ticket}")
            pass
    else:
        logging.debug("No session ticket defined...")