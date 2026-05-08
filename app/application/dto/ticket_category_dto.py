"""Ticket Category DTO"""

from typing import Optional
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TicketCategoryDTO:
    """Data Transfer Object for Ticket Category"""

    id: str
    event_id: str
    name: str
    price: Decimal
    quantity: int
    available: int
    description: Optional[str] = None
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "event_id": self.event_id,
            "name": self.name,
            "price": str(self.price),
            "quantity": self.quantity,
            "available": self.available,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
