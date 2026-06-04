"""Refund DTOs (Data Transfer Objects)"""
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefundDetailResponse:
    """Response DTO for refund details"""
    
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
    """Response DTO for refund summary in a list"""
    
    refund_id: str
    booking_id: str
    refund_amount: float
    status: str
    created_at: str


@dataclass
class RefundListResponse:
    """Response DTO for list of refunds"""
    
    items: List[RefundSummaryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class RefundActionResponse:
    """Response DTO for refund action (approve/reject/payout)"""
    
    refund_id: str
    status: str
    message: str
    timestamp: str


@dataclass
class RefundRequestInput:
    """Input DTO for requesting a refund"""
    
    booking_id: str


@dataclass
class RefundApprovalInput:
    """Input DTO for approving a refund"""
    
    refund_id: str


@dataclass
class RefundRejectionInput:
    """Input DTO for rejecting a refund"""
    
    refund_id: str
    reason: str


@dataclass
class RefundPayoutInput:
    """Input DTO for marking refund as paid out"""
    
    refund_id: str
    payment_reference: str
