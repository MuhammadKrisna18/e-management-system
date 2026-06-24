from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefundDetailResponse:
    
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


@dataclass
class RefundSummaryResponse:
    
    refund_id: str
    booking_id: str
    refund_amount: float
    status: str
    created_at: str


@dataclass
class RefundListResponse:
    
    items: List[RefundSummaryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class RefundActionResponse:
    
    refund_id: str
    status: str
    message: str
    timestamp: str


@dataclass
class RefundRequestInput:
    
    booking_id: str


@dataclass
class RefundApprovalInput:
    
    refund_id: str


@dataclass
class RefundRejectionInput:
    
    refund_id: str
    reason: str


@dataclass
class RefundPayoutInput:
    
    refund_id: str
    payment_reference: str
