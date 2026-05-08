"""Participant DTO"""

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ParticipantDTO:
    """Data Transfer Object for Participant"""

    user_id: str
    name: str
    email: str
    event_id: str
    booking_id: str
    ticket_count: int
    checked_in_count: int = 0
    checked_in_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "event_id": self.event_id,
            "booking_id": self.booking_id,
            "ticket_count": self.ticket_count,
            "checked_in_count": self.checked_in_count,
            "checked_in_at": self.checked_in_at.isoformat() if self.checked_in_at else None,
        }
