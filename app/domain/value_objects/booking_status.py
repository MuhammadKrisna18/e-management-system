"""Booking Status Value Object"""
from enum import Enum


class BookingStatus(Enum):
    """
    Value object representing booking status.
    
    Possible states:
    - PENDING_PAYMENT: Booking created, waiting for payment
    - PAID: Payment completed, booking confirmed
    - EXPIRED: Payment deadline passed without payment
    - REFUNDED: Booking has been refunded
    """
    
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
    
    def __hash__(self):
        return hash(self.value)
