"""Ticket Status Value Object"""
from enum import Enum


class TicketStatus(Enum):
    """
    Value object representing ticket status.
    
    Possible states:
    - ACTIVE: Ticket is valid and can be used for check-in
    - CHECKED_IN: Participant has checked in with this ticket
    - CANCELLED: Ticket has been cancelled (due to refund or event cancellation)
    """
    
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
    
    def __hash__(self):
        return hash(self.value)
