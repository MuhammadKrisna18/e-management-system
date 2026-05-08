"""Get Available Events Query"""

from typing import Optional
from datetime import datetime


class GetAvailableEventsQuery:
    """Query to get available events"""

    def __init__(
        self,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        self.skip = skip
        self.limit = limit
        self.search = search
        self.start_date = start_date
        self.end_date = end_date
