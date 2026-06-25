from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CreateEventRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., gt=0)

class CreateTicketCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., ge=0.0)
    quota: int = Field(..., gt=0)
    sales_start_date: datetime
    sales_end_date: datetime

class EventResponse(BaseModel):
    id: str
    name: str
    status: str
    
    class Config:
        from_attributes = True

class CategorySalesResponse(BaseModel):
    category_name: str
    quota: int
    sold: int
    available: int
    revenue: float

    class Config:
        from_attributes = True

class BookingStatsResponse(BaseModel):
    pending_payment: int
    paid: int
    expired: int
    refunded: int

    class Config:
        from_attributes = True

class EventSalesReportResponse(BaseModel):
    event_id: str
    event_name: str
    category_sales: List[CategorySalesResponse]
    booking_stats: BookingStatsResponse
    total_revenue: float
    report_generated_at: str

    class Config:
        from_attributes = True

class AvailableEventSchema(BaseModel):
    event_id: str
    name: str
    start_date: datetime
    location: str
    lowest_ticket_price: float
    
    class Config:
        from_attributes = True

class AvailableEventsResponse(BaseModel):
    events: List[AvailableEventSchema]

class TicketCategoryDetailSchema(BaseModel):
    name: str
    price: float
    status: str
    
    class Config:
        from_attributes = True

class EventDetailResponse(BaseModel):
    event_id: str
    name: str
    description: str
    start_date: datetime
    location: str
    organizer: str
    ticket_categories: List[TicketCategoryDetailSchema]
    
    class Config:
        from_attributes = True

class ParticipantSchema(BaseModel):
    customer_id: str
    ticket_category: str
    ticket_code: str
    check_in_status: str
    checked_in_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class EventParticipantsResponse(BaseModel):
    event_id: str
    event_name: str
    participants: List[ParticipantSchema]
    total: int
    page: int
    page_size: int
    total_pages: int
    generated_at: str
    
    class Config:
        from_attributes = True
