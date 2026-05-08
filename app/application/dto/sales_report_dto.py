"""Sales Report DTO"""

from typing import Optional, List
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class SalesReportDTO:
    """Data Transfer Object for Sales Report"""

    event_id: str
    event_name: str
    total_bookings: int
    total_tickets_sold: int
    total_revenue: Decimal
    total_refunds: Decimal
    net_revenue: Decimal
    average_ticket_price: Decimal
    category_breakdown: Optional[List[dict]] = None

    def to_dict(self) -> dict:
        """Convert DTO to dictionary"""
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "total_bookings": self.total_bookings,
            "total_tickets_sold": self.total_tickets_sold,
            "total_revenue": str(self.total_revenue),
            "total_refunds": str(self.total_refunds),
            "net_revenue": str(self.net_revenue),
            "average_ticket_price": str(self.average_ticket_price),
            "category_breakdown": self.category_breakdown or [],
        }
