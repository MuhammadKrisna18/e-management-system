from pydantic import BaseModel, Field
from typing import Optional


class RequestRefundRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500)

class RejectRefundRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500)


class RefundResponse(BaseModel):
    refund_id: str
    booking_id: str
    amount: float
    status: str
    requested_at: str
    resolved_at: Optional[str] = None
    reason: str

    class Config:
        from_attributes = True
