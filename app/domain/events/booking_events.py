"""
Booking Domain Events

Events raised during booking lifecycle.
"""

from typing import Optional


class TicketReserved:
    """
    Event raised when ticket is successfully reserved in a booking.
    
    Attributes:
        booking_id: ID of the booking
        quantity: Number of tickets reserved
    """
    
    def __init__(self, booking_id: str, quantity: int = 1) -> None:
        """
        Initialize TicketReserved event.
        
        Args:
            booking_id: ID of the booking
            quantity: Number of tickets reserved
        """
        self.booking_id: str = booking_id
        self.quantity: int = quantity
    
    def __str__(self) -> str:
        return f"TicketReserved(booking_id={self.booking_id}, qty={self.quantity})"
    
    def __repr__(self) -> str:
        return f"TicketReserved({self.booking_id}, {self.quantity})"


class BookingPaid:
    """
    Event raised when booking payment is completed.
    
    Attributes:
        booking_id: ID of the booking
        amount: Payment amount
        payment_reference: Reference from payment gateway
    """
    
    def __init__(
        self,
        booking_id: str,
        amount: float,
        payment_reference: Optional[str] = None
    ) -> None:
        """
        Initialize BookingPaid event.
        
        Args:
            booking_id: ID of the booking
            amount: Payment amount
            payment_reference: Reference from payment gateway
        """
        self.booking_id: str = booking_id
        self.amount: float = amount
        self.payment_reference: Optional[str] = payment_reference
    
    def __str__(self) -> str:
        return f"BookingPaid(booking_id={self.booking_id}, amount={self.amount})"
    
    def __repr__(self) -> str:
        return f"BookingPaid({self.booking_id}, {self.amount})"


class BookingExpired:
    """
    Event raised when booking payment deadline passes.
    
    Attributes:
        booking_id: ID of the booking
    """
    
    def __init__(self, booking_id: str) -> None:
        """
        Initialize BookingExpired event.
        
        Args:
            booking_id: ID of the booking
        """
        self.booking_id: str = booking_id
    
    def __str__(self) -> str:
        return f"BookingExpired(booking_id={self.booking_id})"
    
    def __repr__(self) -> str:
        return f"BookingExpired({self.booking_id})"
