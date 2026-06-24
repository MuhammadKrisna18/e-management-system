
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
    
    def __init__(self, ticket_code: TicketCode, event_id: str) -> None:
        if not isinstance(ticket_code, TicketCode):
            raise TypeError(f"Expected TicketCode, got {type(ticket_code).__name__}")
        
        self.ticket_code: TicketCode = ticket_code
        self.event_id: str = event_id
        self.status: TicketStatus = TicketStatus.ACTIVE
        self.checked_in_at: Optional[datetime] = None
    
    def check_in(self) -> None:
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
        self.status = TicketStatus.CANCELLED
    
    def is_valid_for_event(self) -> bool:
        return self.status == TicketStatus.ACTIVE
    
    def is_checked_in(self) -> bool:
        return self.status == TicketStatus.CHECKED_IN
    
    def is_cancelled(self) -> bool:
        return self.status == TicketStatus.CANCELLED
    
    def __str__(self) -> str:
        return f"Ticket({self.ticket_code}) - {self.status}"
    
    def __repr__(self) -> str:
        return f"Ticket(code={self.ticket_code.code}, status={self.status})"