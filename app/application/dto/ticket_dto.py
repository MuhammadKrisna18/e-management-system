"""Ticket DTO"""

from typing import Optional
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TicketDTO:
    """Data Transfer Object for Ticket"""

    id: str
    booking_id: str
    ticket_category_id: str
    ticket_code: str
    status: str
    price: Decimal
    checked_in: bool = False
    checked_in_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "ticket_category_id": self.ticket_category_id,
            "ticket_code": self.ticket_code,
            "status": self.status,
            "price": str(self.price),
            "checked_in": self.checked_in,
            "checked_in_at": self.checked_in_at.isoformat() if self.checked_in_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
