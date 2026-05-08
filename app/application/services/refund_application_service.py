"""Refund Application Service"""

from decimal import Decimal
from app.application.dto.refund_dto import RefundDTO
from app.application.commands.request_refund_command import RequestRefundCommand
from app.application.commands.approve_refund_command import ApproveRefundCommand
from app.application.commands.reject_refund_command import RejectRefundCommand
from app.application.commands.payout_refund_command import PayoutRefundCommand


class RefundApplicationService:
    """Application service for refund operations"""

    def __init__(
        self,
        request_refund_handler,
        approve_refund_handler,
        reject_refund_handler,
        payout_refund_handler,
        refund_repository,
    ):
        self.request_refund_handler = request_refund_handler
        self.approve_refund_handler = approve_refund_handler
        self.reject_refund_handler = reject_refund_handler
        self.payout_refund_handler = payout_refund_handler
        self.refund_repository = refund_repository

    def request_refund(
        self,
        booking_id: str,
        amount: Decimal,
        reason: str,
    ) -> str:
        """Request a refund"""
        command = RequestRefundCommand(
            booking_id=booking_id,
            amount=amount,
            reason=reason,
        )
        return self.request_refund_handler.handle(command)

    def approve_refund(self, refund_id: str, notes: str = "") -> None:
        """Approve a refund"""
        command = ApproveRefundCommand(refund_id=refund_id, notes=notes)
        self.approve_refund_handler.handle(command)

    def reject_refund(self, refund_id: str, reason: str) -> None:
        """Reject a refund"""
        command = RejectRefundCommand(refund_id=refund_id, reason=reason)
        self.reject_refund_handler.handle(command)

    def payout_refund(self, refund_id: str) -> None:
        """Payout a refund"""
        command = PayoutRefundCommand(refund_id=refund_id)
        self.payout_refund_handler.handle(command)

    def get_refund_status(self, refund_id: str) -> dict:
        """Get refund status"""
        refund = self.refund_repository.get_by_id(refund_id)
        return refund.to_dict() if refund else None
