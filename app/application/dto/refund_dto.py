"""Refund DTO"""

from typing import Optional
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class RefundDTO:
    """Data Transfer Object for Refund"""

    id: str
    booking_id: str
    amount: Decimal
    reason: str
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "amount": str(self.amount),
            "reason": self.reason,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
