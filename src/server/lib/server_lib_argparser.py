#
# Server side code
#
# Ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_server.py
# Ref: https://aioquic.readthedocs.io/en/latest/asyncio.html
# Ref: https://aioquic.readthedocs.io/en/latest/quic.html#module-aioquic.quic.configuration
#

import argparse

def get_args_parser(protocol_name: str):
    # protocol_name example : 'DNS over QUIC'

    parser = argparse.ArgumentParser(description=protocol_name)
    parser.add_argument(
        "--host",
        type=str,
        default="::",
        help="listen on the specified address (defaults to ::)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=853,
        help="listen on the specified port (defaults to 853)",
    )
    parser.add_argument(
        "-k",
        "--private-key",
        type=str,
        help="load the TLS private key from the specified file",
    )
    parser.add_argument(
        "-c",
        "--certificate",
        type=str,
        required=True,
        help="load the TLS certificate from the specified file",
    )
    parser.add_argument(
        "--retry",
        action="store_true",
        help="send a retry for new connections (defaults to False)",
    )
    parser.add_argument(
        "-q",
        "--quic-log",
        type=str,
        help="log QUIC events to QLOG files in the specified directory (defaults to None)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase logging verbosity"
    )

    return parser.parse_args()