from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# ── Request schemas ──────────────────────────────────────────────────────────

class CreateBookingRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)
    ticket_category_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class PayBookingRequest(BaseModel):
    amount: float = Field(..., gt=0.0)


class CheckInTicketRequest(BaseModel):
    ticket_code: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)


class CalculatePriceRequest(BaseModel):
    event_id: str
    ticket_category_name: str
    quantity: int = Field(..., gt=0)


# ── Response schemas ─────────────────────────────────────────────────────────

class CalculatePriceResponse(BaseModel):
    total_price: float


class BookingResponse(BaseModel):
    booking_id: str
    customer_id: str
    event_id: str
    ticket_category_name: str
    quantity: int
    total_price: float
    status: str
    payment_deadline: datetime

    class Config:
        from_attributes = True


class TicketResponse(BaseModel):
    ticket_code: str
    event_id: str
    status: str
    checked_in_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PurchasedTicketResponse(BaseModel):
    ticket_code: str
    event_id: str
    event_name: str
    ticket_category: str
    status: str

    class Config:
        from_attributes = True


class PurchasedTicketsResponse(BaseModel):
    customer_id: str
    tickets: List[PurchasedTicketResponse]

    class Config:
        from_attributes = True


class CheckInResponse(BaseModel):
    ticket_code: str
    message: str
