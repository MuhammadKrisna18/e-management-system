"""Ticket Repository Interface"""
from abc import ABC
from abc import abstractmethod
from typing import List, Optional


class TicketRepository(ABC):
    """
    Repository interface for Ticket entities.
    
    Defines the contract for ticket persistence operations.
    """

    @abstractmethod
    def save(self, ticket) -> str:
        """
        Save or update a ticket.
        
        Args:
            ticket: Ticket entity instance
            
        Returns:
            str: Ticket ID or code
        """
        pass

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[object]:
        """
        Retrieve a ticket by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            Ticket entity or None if not found
        """
        pass

    @abstractmethod
    def find_by_booking(self, booking_id: str) -> List[object]:
        """
        Find all tickets for a booking.
        
        Args:
            booking_id: Booking identifier
            
        Returns:
            List of Ticket entities
        """
        pass

    @abstractmethod
    def find_by_code(self, ticket_code: str) -> Optional[object]:
        """
        Find ticket by ticket code.
        
        Args:
            ticket_code: Unique ticket code
            
        Returns:
            Ticket entity or None if not found
        """
        pass

    @abstractmethod
    def find_by_event(self, event_id: str) -> List[object]:
        """
        Find all tickets for an event.
        
        Args:
            event_id: Event identifier
            
        Returns:
            List of Ticket entities
        """
        pass

    @abstractmethod
    def find_all(self) -> List[object]:
        """
        Find all tickets.
        
        Returns:
            List of all Ticket entities
        """
        pass

    @abstractmethod
    def delete(self, ticket_id: str) -> bool:
        """
        Delete a ticket by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        pass
