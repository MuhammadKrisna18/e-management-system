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
