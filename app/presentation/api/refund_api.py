from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.config.container import get_container, Container
from app.presentation.schemas.refund_schemas import (
    RequestRefundRequest,
    RejectRefundRequest,
    RefundResponse
)
from app.application.commands.request_refund_command import RequestRefundCommand
from app.application.commands.approve_refund_command import ApproveRefundCommand
from app.application.commands.reject_refund_command import RejectRefundCommand
from app.application.commands.mark_refund_payout_command import MarkRefundPayoutCommand

router = APIRouter(prefix="/refunds", tags=["Refunds"])

def get_app_container() -> Container:
    return get_container()

@router.post("/booking/{booking_id}", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
def request_refund(
    booking_id: str,
    request: RequestRefundRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = RequestRefundCommand(
            booking_id=booking_id,
            reason=request.reason
        )
        handler = container.get_request_refund_handler()
        refund_aggregate = handler.handle(command)
        return refund_aggregate.refund
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{refund_id}/approve", response_model=RefundResponse)
def approve_refund(
    refund_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = ApproveRefundCommand(refund_id=refund_id)
        handler = container.get_approve_refund_handler()
        refund_aggregate = handler.handle(command)
        return refund_aggregate.refund
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{refund_id}/reject", response_model=RefundResponse)
def reject_refund(
    refund_id: str,
    request: RejectRefundRequest,
    container: Container = Depends(get_app_container)
):
    try:
        command = RejectRefundCommand(
            refund_id=refund_id,
            reason=request.reason
        )
        handler = container.get_reject_refund_handler()
        refund_aggregate = handler.handle(command)
        return refund_aggregate.refund
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{refund_id}/payout", response_model=RefundResponse)
def mark_refund_payout(
    refund_id: str,
    container: Container = Depends(get_app_container)
):
    try:
        command = MarkRefundPayoutCommand(refund_id=refund_id)
        handler = container.get_mark_refund_payout_handler()
        refund_aggregate = handler.handle(command)
        return refund_aggregate.refund
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
