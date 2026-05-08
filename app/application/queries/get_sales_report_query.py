"""Get Sales Report Query"""

from typing import Optional
from datetime import datetime


class GetSalesReportQuery:
    """Query to get sales report"""

    def __init__(
        self,
        event_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        self.event_id = event_id
        self.start_date = start_date
        self.end_date = end_date
