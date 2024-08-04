import asyncio
import logging
import pickle
from typing import cast
import time

from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration

from lib.client_lib_argparser import get_args_parser, set_quic_configuration
from lib.client_lib_log import set_quic_logging

## [SHOULD BE MODIFIED] defines server side service protocol
from lib.client_lib_chattingprotocol import get_protocol_class, get_protocol_name, get_protocol_alpn

#
# main function
#
# ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_client.py
#

def save_session_ticket(ticket):
    """
    Callback which is invoked by the TLS engine when a new session ticket is received.
    """
    logging.info("New session ticket received")
    if args.session_ticket:
        with open(args.session_ticket, "wb") as fp:
            pickle.dump(ticket, fp)

#
# main function
#
# ref: https://aioquic.readthedocs.io/en/latest/asyncio.html
#

async def main(
    configuration: QuicConfiguration,
    host: str,
    port: int,
) -> None:

    #
    # activate server process
    #  

    logging.info(f"Connecting to {host}:{port}")
    
    async with connect(
        host,
        port,
        configuration=configuration,
        session_ticket_handler=save_session_ticket,
        create_protocol=get_protocol_class(),
    ) as client:
        
        await client.activate_protocol()

#
# main procedure for client configuration and activation
#
# ref: https://aioquic.readthedocs.io/en/latest/quic.html#module-aioquic.quic.configuration
#

if __name__ == "__main__":

    #
    # defines name and alpn (id) of service
    #

    ## defines name of service
    name_of_service = get_protocol_name()

    ## defines alpn identifier of service 
    alpn_of_service = get_protocol_alpn()

    #
    # configures cli args and logging options
    #

    args = get_args_parser(name_of_service)
    set_quic_logging(args)

    #
    # configures QUIC protocol
    #

    configuration = QuicConfiguration(alpn_protocols=[alpn_of_service], is_client=True)
    set_quic_configuration(configuration, args)

    #
    # executes client
    #

    try:
        asyncio.run(
            main(
                configuration=configuration,
                host=args.host,
                port=args.port,
            )
        )
    except KeyboardInterrupt:
        logging.info('Client terminated ...')