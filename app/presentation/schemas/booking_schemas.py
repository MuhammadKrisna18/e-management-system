from pydantic import BaseModel, Field
from typing import List
class CreateBookingRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)
    ticket_category_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class PayBookingRequest(BaseModel):
    payment_amount: float = Field(..., gt=0.0)

class CalculatePriceRequest(BaseModel):
    event_id: str
    ticket_category_name: str
    quantity: int = Field(..., gt=0)

class CalculatePriceResponse(BaseModel):
    total_price: float


class BookingResponse(BaseModel):
    id: str
    status: str
    total_price: float

    class Config:
        from_attributes = True

class TicketResponse(BaseModel):
    code: str
    status: str

    class Config:
        from_attributes = True

class PurchasedTicketSchema(BaseModel):
    ticket_code: str
    event_id: str
    event_name: str
    ticket_category: str
    status: str
    
    class Config:
        from_attributes = True

class PurchasedTicketsResponse(BaseModel):
    customer_id: str
    tickets: List[PurchasedTicketSchema]
    
    class Config:
        from_attributes = True
