"""Event DTO"""

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class EventDTO:
    """Data Transfer Object for Event"""

    id: str
    name: str
    description: str
    location: str
    start_date: datetime
    end_date: datetime
    organizer_id: str
    max_capacity: int
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "organizer_id": self.organizer_id,
            "max_capacity": self.max_capacity,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
