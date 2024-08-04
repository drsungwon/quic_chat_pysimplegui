import asyncio
import logging

from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

from lib.server_lib_tls import SessionTicketStore
from lib.server_lib_argparser import get_args_parser
from lib.server_lib_log import get_quic_logger

## [SHOULD BE MODIFIED] defines server side service protocol
from lib.server_lib_chattingprotocol import get_protocol_class, get_protocol_name, get_protocol_alpn
from lib.server_lib_chattingprotocol import save_quic_server_pointer

#
# main function
#
# ref: https://aioquic.readthedocs.io/en/latest/asyncio.html
#

async def main(
    host: str,
    port: int,
    configuration: QuicConfiguration,
    session_ticket_store: SessionTicketStore,
    retry: bool,
) -> None:

    #
    # activate server process
    #   

    logging.info('Server atarted ...')

    quicserver_ptr = await serve(
        host,
        port,
        configuration=configuration,
        create_protocol=get_protocol_class(), 
        session_ticket_fetcher=session_ticket_store.pop,
        session_ticket_handler=session_ticket_store.add,
        retry=retry,
    )

    save_quic_server_pointer(quicserver_ptr)

    await asyncio.Future()

#
# main procedure for server configuration and activation
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
    quic_logger = get_quic_logger(args)

    #
    # configures QUIC protocol
    #

    configuration = QuicConfiguration(
        ## 'doq' for test purpose will be removed (DNS over QUIC) 
        alpn_protocols=[alpn_of_service], 
        is_client=False,
        quic_logger=quic_logger,
    )

    configuration.load_cert_chain(
        args.certificate, 
        args.private_key
    )

    #
    # executes server
    #

    try:
        asyncio.run(
            main(
                host=args.host,
                port=args.port,
                configuration=configuration,
                session_ticket_store=SessionTicketStore(),
                retry=args.retry,
            )
        )
    except KeyboardInterrupt:
        logging.info('Server terminated ...')