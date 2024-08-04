# 
# Server side code
#
# Ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_server.py
#

from aioquic.tls import SessionTicket
from typing import Dict, Optional

class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: Dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> Optional[SessionTicket]:
        return self.tickets.pop(label, None)
   