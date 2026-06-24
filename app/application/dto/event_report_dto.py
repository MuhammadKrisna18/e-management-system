from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class CategorySalesDto:
    
    category_name: str
    quota: int
    sold: int
    available: int
    revenue: float = 0.0


@dataclass
class BookingStatsDto:
    
    pending_payment: int
    paid: int
    expired: int
    refunded: int


@dataclass
class EventSalesReportResponse:
    
    event_id: str
    event_name: str
    category_sales: List[CategorySalesDto]
    booking_stats: BookingStatsDto
    total_revenue: float
    report_generated_at: str


@dataclass
class ParticipantDto:
    
    customer_id: str
    ticket_category: str
    ticket_code: str
    check_in_status: str
    checked_in_at: Optional[str] = None


@dataclass
class EventParticipantsResponse:
    
    event_id: str
    event_name: str
    participants: List[ParticipantDto]
    total: int
    page: int
    page_size: int
    total_pages: int
    generated_at: str
