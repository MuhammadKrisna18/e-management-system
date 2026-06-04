"""Refund Status Value Object"""
from enum import Enum


class RefundStatus(Enum):
    """
    Value object representing refund status.
    
    Possible states:
    - REQUESTED: Refund request submitted
    - APPROVED: Refund request approved by organizer
    - REJECTED: Refund request rejected by organizer
    - PAID_OUT: Refund has been processed and paid out to customer
    """
    
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
    
    def __hash__(self):
        return hash(self.value)
