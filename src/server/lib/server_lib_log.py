# 
# Server side code
#
# Ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_server.py
#

import logging

from aioquic.quic.logger import QuicFileLogger

def get_quic_logger(args):

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    # create QUIC logger
    if args.quic_log:
        quic_logger = QuicFileLogger(args.quic_log)
    else:
        quic_logger = None