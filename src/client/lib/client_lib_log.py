# 
# Client side code
#
# Ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_client.py
#

import logging

def set_quic_logging(args):

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )