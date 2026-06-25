from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.refund_schemas import (
    RejectRefundRequest,
    MarkRefundPayoutRequest,
    RefundResponse,
    RefundListResponse,
)
from app.application.commands.request_refund_command import RequestRefundCommand
from app.application.commands.approve_refund_command import ApproveRefundCommand
from app.application.commands.reject_refund_command import RejectRefundCommand
from app.application.commands.mark_refund_payout_command import MarkRefundPayoutCommand
from app.application.queries.refund_queries import (
    GetRefundDetailsQuery,
    GetCustomerRefundsQuery,
    GetApprovedRefundsQuery,
)

router = APIRouter(tags=["Refunds"])


def get_app_container() -> Container:
    return get_container()


def _map_refund(refund) -> dict:
    status_val = refund.status.value if hasattr(refund.status, "value") else str(refund.status)
    return {
        "refund_id": refund.refund_id,
        "booking_id": refund.booking_id,
        "customer_id": refund.customer_id,
        "event_id": refund.event_id,
        "refund_amount": refund.refund_amount.amount if hasattr(refund.refund_amount, "amount") else float(refund.refund_amount),
        "status": status_val,
        "created_at": refund.created_at.isoformat(),
        "refund_deadline": refund.refund_deadline.isoformat() if hasattr(refund.refund_deadline, "isoformat") else str(refund.refund_deadline),
        "rejection_reason": refund.rejection_reason,
        "payment_reference": refund.payment_reference,
        "approved_at": refund.approved_at.isoformat() if refund.approved_at else None,
        "rejected_at": refund.rejected_at.isoformat() if refund.rejected_at else None,
        "paid_out_at": refund.paid_out_at.isoformat() if refund.paid_out_at else None,
    }


# ── US15: Request Refund ──────────────────────────────────────────────────────

@router.post(
    "/bookings/{booking_id}/refund",
    response_model=RefundResponse,
    status_code=status.HTTP_201_CREATED,
    summary="US15 - Request Refund",
)
def request_refund(
    booking_id: str,
    container: Container = Depends(get_app_container),
):
    """Request a refund for a paid booking. Tickets must not be checked in."""
    try:
        command = RequestRefundCommand(booking_id=booking_id)
        refund_id = container.get_request_refund_handler().handle(command)
        # Retrieve full refund to return
        from app.application.queries.refund_queries import GetRefundDetailsQuery
        query = GetRefundDetailsQuery(refund_id=refund_id)
        detail = container.get_refund_details_handler().handle(query)
        return {
            "refund_id": detail.refund_id,
            "booking_id": detail.booking_id,
            "customer_id": detail.customer_id,
            "event_id": detail.event_id,
            "refund_amount": detail.refund_amount,
            "status": detail.status,
            "created_at": detail.created_at,
            "refund_deadline": detail.refund_deadline,
            "rejection_reason": detail.rejection_reason,
            "payment_reference": detail.payment_reference,
            "approved_at": detail.approved_at,
            "rejected_at": detail.rejected_at,
            "paid_out_at": detail.paid_out_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US15: Get Refund Details ──────────────────────────────────────────────────

@router.get(
    "/refunds/{refund_id}",
    response_model=RefundResponse,
    summary="US15 - Get Refund Details",
)
def get_refund_details(
    refund_id: str,
    container: Container = Depends(get_app_container),
):
    """Get details of a specific refund."""
    try:
        query = GetRefundDetailsQuery(refund_id=refund_id)
        detail = container.get_refund_details_handler().handle(query)
        return {
            "refund_id": detail.refund_id,
            "booking_id": detail.booking_id,
            "customer_id": detail.customer_id,
            "event_id": detail.event_id,
            "refund_amount": detail.refund_amount,
            "status": detail.status,
            "created_at": detail.created_at,
            "refund_deadline": detail.refund_deadline,
            "rejection_reason": detail.rejection_reason,
            "payment_reference": detail.payment_reference,
            "approved_at": detail.approved_at,
            "rejected_at": detail.rejected_at,
            "paid_out_at": detail.paid_out_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── US15: Get Customer Refunds ────────────────────────────────────────────────

@router.get(
    "/customers/{customer_id}/refunds",
    response_model=RefundListResponse,
    summary="US15 - Get Customer Refunds",
)
def get_customer_refunds(
    customer_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    container: Container = Depends(get_app_container),
):
    """Get all refunds for a customer with pagination."""
    query = GetCustomerRefundsQuery(customer_id=customer_id, page=page, page_size=page_size)
    result = container.get_customer_refunds_handler().handle(query)
    return {
        "items": [
            {
                "refund_id": item.refund_id,
                "booking_id": item.booking_id,
                "refund_amount": item.refund_amount,
                "status": item.status,
                "created_at": item.created_at,
            }
            for item in result.items
        ],
        "total": result.total,
        "page": result.page,
        "page_size": result.page_size,
        "total_pages": result.total_pages,
    }


# ── US16: Approve Refund ──────────────────────────────────────────────────────

@router.post(
    "/refunds/{refund_id}/approve",
    response_model=RefundResponse,
    summary="US16 - Approve Refund",
)
def approve_refund(
    refund_id: str,
    container: Container = Depends(get_app_container),
):
    """Approve a refund request. Booking is marked Refunded and tickets cancelled."""
    try:
        command = ApproveRefundCommand(refund_id=refund_id)
        container.get_approve_refund_handler().handle(command)
        query = GetRefundDetailsQuery(refund_id=refund_id)
        detail = container.get_refund_details_handler().handle(query)
        return {
            "refund_id": detail.refund_id,
            "booking_id": detail.booking_id,
            "customer_id": detail.customer_id,
            "event_id": detail.event_id,
            "refund_amount": detail.refund_amount,
            "status": detail.status,
            "created_at": detail.created_at,
            "refund_deadline": detail.refund_deadline,
            "rejection_reason": detail.rejection_reason,
            "payment_reference": detail.payment_reference,
            "approved_at": detail.approved_at,
            "rejected_at": detail.rejected_at,
            "paid_out_at": detail.paid_out_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US17: Reject Refund ───────────────────────────────────────────────────────

@router.post(
    "/refunds/{refund_id}/reject",
    response_model=RefundResponse,
    summary="US17 - Reject Refund",
)
def reject_refund(
    refund_id: str,
    request: RejectRefundRequest,
    container: Container = Depends(get_app_container),
):
    """Reject a refund request with a reason."""
    try:
        command = RejectRefundCommand(refund_id=refund_id, reason=request.reason)
        container.get_reject_refund_handler().handle(command)
        query = GetRefundDetailsQuery(refund_id=refund_id)
        detail = container.get_refund_details_handler().handle(query)
        return {
            "refund_id": detail.refund_id,
            "booking_id": detail.booking_id,
            "customer_id": detail.customer_id,
            "event_id": detail.event_id,
            "refund_amount": detail.refund_amount,
            "status": detail.status,
            "created_at": detail.created_at,
            "refund_deadline": detail.refund_deadline,
            "rejection_reason": detail.rejection_reason,
            "payment_reference": detail.payment_reference,
            "approved_at": detail.approved_at,
            "rejected_at": detail.rejected_at,
            "paid_out_at": detail.paid_out_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US18: Mark Refund as Paid Out ─────────────────────────────────────────────

@router.post(
    "/refunds/{refund_id}/payout",
    response_model=RefundResponse,
    summary="US18 - Mark Refund as Paid Out",
)
def mark_refund_payout(
    refund_id: str,
    request: MarkRefundPayoutRequest,
    container: Container = Depends(get_app_container),
):
    """Mark an approved refund as paid out to the customer."""
    try:
        command = MarkRefundPayoutCommand(
            refund_id=refund_id,
            payment_reference=request.payment_reference,
        )
        container.get_mark_refund_payout_handler().handle(command)
        query = GetRefundDetailsQuery(refund_id=refund_id)
        detail = container.get_refund_details_handler().handle(query)
        return {
            "refund_id": detail.refund_id,
            "booking_id": detail.booking_id,
            "customer_id": detail.customer_id,
            "event_id": detail.event_id,
            "refund_amount": detail.refund_amount,
            "status": detail.status,
            "created_at": detail.created_at,
            "refund_deadline": detail.refund_deadline,
            "rejection_reason": detail.rejection_reason,
            "payment_reference": detail.payment_reference,
            "approved_at": detail.approved_at,
            "rejected_at": detail.rejected_at,
            "paid_out_at": detail.paid_out_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── US18: Get Approved Refunds (Admin) ───────────────────────────────────────

@router.get(
    "/refunds/approved/pending-payout",
    response_model=RefundListResponse,
    summary="US18 - Get Approved Refunds Pending Payout",
)
def get_approved_refunds(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    container: Container = Depends(get_app_container),
):
    """Get all approved refunds that are pending payout (admin use)."""
    query = GetApprovedRefundsQuery(page=page, page_size=page_size)
    result = container.get_approved_refunds_handler().handle(query)
    return {
        "items": [
            {
                "refund_id": item.refund_id,
                "booking_id": item.booking_id,
                "refund_amount": item.refund_amount,
                "status": item.status,
                "created_at": item.created_at,
            }
            for item in result.items
        ],
        "total": result.total,
        "page": result.page,
        "page_size": result.page_size,
        "total_pages": result.total_pages,
    }
