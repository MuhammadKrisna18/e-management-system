"""Booking DTO"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class BookingDTO:
    """Data Transfer Object for Booking"""

    id: str
    user_id: str
    event_id: str
    attendee_name: str
    attendee_email: str
    total_price: Decimal
    status: str
    ticket_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "attendee_name": self.attendee_name,
            "attendee_email": self.attendee_email,
            "total_price": str(self.total_price),
            "status": self.status,
            "ticket_count": self.ticket_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
