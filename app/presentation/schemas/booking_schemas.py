from pydantic import BaseModel, Field

class CreateBookingRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    event_id: str = Field(..., min_length=1)
    ticket_category_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class PayBookingRequest(BaseModel):
    payment_amount: float = Field(..., gt=0.0)

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
