
from typing import Optional


class TicketReserved:
    
    def __init__(
        self,
        booking_id: str,
        event_id: str,
        ticket_category: str,
        quantity: int,
        total_price: float
    ) -> None:
        self.booking_id: str = booking_id
        self.event_id: str = event_id
        self.ticket_category: str = ticket_category
        self.quantity: int = quantity
        self.total_price: float = total_price
    
    def __str__(self) -> str:
        return f"TicketReserved(booking_id={self.booking_id}, qty={self.quantity})"
    
    def __repr__(self) -> str:
        return f"TicketReserved({self.booking_id}, {self.quantity})"


class BookingPaid:
    
    def __init__(
        self,
        booking_id: str,
        amount: float,
        payment_reference: Optional[str] = None
    ) -> None:
        self.booking_id: str = booking_id
        self.amount: float = amount
        self.payment_reference: Optional[str] = payment_reference
    
    def __str__(self) -> str:
        return f"BookingPaid(booking_id={self.booking_id}, amount={self.amount})"
    
    def __repr__(self) -> str:
        return f"BookingPaid({self.booking_id}, {self.amount})"


class BookingExpired:
    
    def __init__(self, booking_id: str) -> None:
        self.booking_id: str = booking_id
    
    def __str__(self) -> str:
        return f"BookingExpired(booking_id={self.booking_id})"
    
    def __repr__(self) -> str:
        return f"BookingExpired({self.booking_id})"
