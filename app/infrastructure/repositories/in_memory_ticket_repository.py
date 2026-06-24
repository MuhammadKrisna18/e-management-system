from typing import Dict, List, Optional
from app.domain.repositories.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):

    def __init__(self):
        self._tickets: Dict[str, object] = {}
        self._ticket_counter = 0

    def save(self, ticket) -> str:
        if not hasattr(ticket, 'ticket_id'):
            ticket.ticket_id = self._generate_ticket_id()
        
        ticket_id = ticket.ticket_id
        self._tickets[ticket_id] = ticket
        return ticket_id

    def get_by_id(self, ticket_id: str) -> Optional[object]:
        return self._tickets.get(ticket_id)

    def find_by_booking(self, booking_id: str) -> List[object]:
        return [
            ticket for ticket in self._tickets.values()
            if hasattr(ticket, 'booking_id') and ticket.booking_id == booking_id
        ]

    def find_by_code(self, ticket_code: str) -> Optional[object]:
        for ticket in self._tickets.values():
            if (hasattr(ticket, 'ticket_code') and 
                hasattr(ticket.ticket_code, 'value') and
                ticket.ticket_code.value == ticket_code):
                return ticket
            # Fallback for simple code attribute
            elif hasattr(ticket, 'code') and ticket.code == ticket_code:
                return ticket
        return None

    def find_by_event(self, event_id: str) -> List[object]:
        return [
            ticket for ticket in self._tickets.values()
            if hasattr(ticket, 'event_id') and ticket.event_id == event_id
        ]

    def find_all(self) -> List[object]:
        return list(self._tickets.values())

    def delete(self, ticket_id: str) -> bool:
        if ticket_id in self._tickets:
            del self._tickets[ticket_id]
            return True
        return False

    def _generate_ticket_id(self) -> str:
        self._ticket_counter += 1
        return f"TKT{self._ticket_counter:06d}"
