"""In-Memory Ticket Repository Implementation"""
from typing import Dict, List, Optional
from app.domain.repositories.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    """
    In-memory implementation of TicketRepository.
    Stores Ticket entities in memory for development and testing.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self._tickets: Dict[str, object] = {}
        self._ticket_counter = 0

    def save(self, ticket) -> str:
        """
        Save ticket.
        
        Args:
            ticket: Ticket entity to save
            
        Returns:
            str: Ticket code/ID
        """
        if not hasattr(ticket, 'ticket_id'):
            ticket.ticket_id = self._generate_ticket_id()
        
        ticket_id = ticket.ticket_id
        self._tickets[ticket_id] = ticket
        return ticket_id

    def get_by_id(self, ticket_id: str) -> Optional[object]:
        """
        Retrieve ticket by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            Ticket entity or None if not found
        """
        return self._tickets.get(ticket_id)

    def find_by_booking(self, booking_id: str) -> List[object]:
        """
        Find all tickets for a booking.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            List of Ticket entities
        """
        return [
            ticket for ticket in self._tickets.values()
            if hasattr(ticket, 'booking_id') and ticket.booking_id == booking_id
        ]

    def find_by_code(self, ticket_code: str) -> Optional[object]:
        """
        Find ticket by ticket code.
        
        Args:
            ticket_code: Unique ticket code
            
        Returns:
            Ticket entity or None if not found
        """
        for ticket in self._tickets.values():
            if (hasattr(ticket, 'ticket_code') and 
                hasattr(ticket.ticket_code, 'code') and
                ticket.ticket_code.code == ticket_code):
                return ticket
            # Fallback for simple code attribute
            elif hasattr(ticket, 'code') and ticket.code == ticket_code:
                return ticket
        return None

    def find_by_event(self, event_id: str) -> List[object]:
        """
        Find all tickets for an event.
        
        Args:
            event_id: Event identifier
            
        Returns:
            List of Ticket entities
        """
        return [
            ticket for ticket in self._tickets.values()
            if hasattr(ticket, 'event_id') and ticket.event_id == event_id
        ]

    def find_all(self) -> List[object]:
        """
        Find all tickets.
        
        Returns:
            List of all Ticket entities
        """
        return list(self._tickets.values())

    def delete(self, ticket_id: str) -> bool:
        """
        Delete a ticket by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if ticket_id in self._tickets:
            del self._tickets[ticket_id]
            return True
        return False

    def _generate_ticket_id(self) -> str:
        """
        Generate unique ticket ID.
        
        Returns:
            str: Generated ticket ID
        """
        self._ticket_counter += 1
        return f"TKT{self._ticket_counter:06d}"
