from pydantic import BaseModel, Field
from typing import List, Optional


# ── Request schemas ──────────────────────────────────────────────────────────

class RequestRefundRequest(BaseModel):
    pass  # booking_id comes from path param


class RejectRefundRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500)


class MarkRefundPayoutRequest(BaseModel):
    payment_reference: str = Field(..., min_length=1)


# ── Response schemas ─────────────────────────────────────────────────────────

class RefundResponse(BaseModel):
    refund_id: str
    booking_id: str
    customer_id: str
    event_id: str
    refund_amount: float
    status: str
    created_at: str
    refund_deadline: str
    rejection_reason: Optional[str] = None
    payment_reference: Optional[str] = None
    approved_at: Optional[str] = None
    rejected_at: Optional[str] = None
    paid_out_at: Optional[str] = None

    class Config:
        from_attributes = True


class RefundSummaryResponse(BaseModel):
    refund_id: str
    booking_id: str
    refund_amount: float
    status: str
    created_at: str

    class Config:
        from_attributes = True


class RefundListResponse(BaseModel):
    items: List[RefundSummaryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
