"""Create Event Command"""

from typing import Optional
from datetime import datetime


class CreateEventCommand:
    """Command to create a new event"""

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        start_date: datetime,
        end_date: datetime,
        organizer_id: str,
        max_capacity: int,
        status: str = "DRAFT",
    ):
        self.name = name
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.organizer_id = organizer_id
        self.max_capacity = max_capacity
        self.status = status
