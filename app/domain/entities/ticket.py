"""
Ticket Entity

Represents an individual ticket for an event.
Manages ticket lifecycle including check-in status.
"""

from datetime import datetime
from typing import Optional

from app.domain.constants import TicketStatuses, ErrorMessages
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.ticket_status import TicketStatus
from app.domain.exceptions import (
    TicketAlreadyCheckedException,
    InvalidTicketStatusException,
)


class Ticket:
    """
    Entity representing a ticket for an event.
    
    A ticket is issued after successful payment of a booking.
    It has a unique ticket code and can be checked in for attendance.
    """
    
    def __init__(self, ticket_code: TicketCode) -> None:
        """
        Initialize Ticket entity.
        
        Args:
            ticket_code: TicketCode value object with unique code
            
        Raises:
            TypeError: If ticket_code is not TicketCode instance
        """
        if not isinstance(ticket_code, TicketCode):
            raise TypeError(f"Expected TicketCode, got {type(ticket_code).__name__}")
        
        self.ticket_code: TicketCode = ticket_code
        self.status: TicketStatus = TicketStatus.ACTIVE
        self.checked_in_at: Optional[datetime] = None
    
    def check_in(self) -> None:
        """
        Mark ticket as checked in for event attendance.
        
        Changes status from ACTIVE to CHECKED_IN.
        Records the check-in timestamp.
        
        Raises:
            TicketAlreadyCheckedException: If already checked in
            InvalidTicketStatusException: If ticket is cancelled
        """
        if self.status == TicketStatus.CHECKED_IN:
            raise TicketAlreadyCheckedException(
                ErrorMessages.TICKET_ALREADY_CHECKED_IN
            )
        
        if self.status == TicketStatus.CANCELLED:
            raise InvalidTicketStatusException(
                ErrorMessages.TICKET_CANNOT_CHECK_IN_CANCELLED
            )
        
        self.status = TicketStatus.CHECKED_IN
        self.checked_in_at = datetime.now()
    
    def cancel(self) -> None:
        """
        Cancel this ticket.
        
        Used when booking is refunded or event is cancelled.
        Cancelled tickets cannot be used for check-in.
        """
        self.status = TicketStatus.CANCELLED
    
    def is_valid_for_event(self) -> bool:
        """
        Check if ticket is valid for event check-in.
        
        Returns:
            bool: True if status is ACTIVE
        """
        return self.status == TicketStatus.ACTIVE
    
    def is_checked_in(self) -> bool:
        """
        Check if ticket has been used for check-in.
        
        Returns:
            bool: True if status is CHECKED_IN
        """
        return self.status == TicketStatus.CHECKED_IN
    
    def is_cancelled(self) -> bool:
        """
        Check if ticket has been cancelled.
        
        Returns:
            bool: True if status is CANCELLED
        """
        return self.status == TicketStatus.CANCELLED
    
    def __str__(self) -> str:
        """String representation showing code and status."""
        return f"Ticket({self.ticket_code}) - {self.status}"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"Ticket(code={self.ticket_code.code}, status={self.status})"