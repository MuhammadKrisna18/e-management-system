from app.domain.repositories.refund_repository import RefundRepository
from app.application.interfaces.refund_payment_service import RefundPaymentService


class MarkRefundPayoutHandler:

    def __init__(
        self,
        refund_repository: RefundRepository,
        refund_payment_service: RefundPaymentService = None
    ):
        self.refund_repository = refund_repository
        self.refund_payment_service = refund_payment_service

    def handle(self, command) -> dict:
        # Get refund
        refund_agg = self.refund_repository.get_by_id(command.refund_id)
        if not refund_agg:
            raise ValueError(f"Refund {command.refund_id} not found")

        refund = refund_agg.refund

        # Validation: Refund must be in Approved status
        if refund.status != "Approved":
            raise ValueError(
                f"Refund can only be marked as paid out if in Approved status. "
                f"Current status: {refund.status}"
            )

        # Validation: Payment reference must be provided
        if not hasattr(command, 'payment_reference') or not command.payment_reference:
            raise ValueError("Payment reference must be recorded")

        # Verify refund with payment service if available
        if self.refund_payment_service:
            status = self.refund_payment_service.verify_refund_status(
                command.payment_reference
            )
            if status not in ("processed", "completed"):
                raise ValueError(
                    f"Payment verification failed. Status: {status}"
                )

        # Mark refund as paid out
        refund_agg.mark_as_paid_out(command.payment_reference)

        # Save refund
        self.refund_repository.save(refund_agg)

        return {
            "refund_id": refund.refund_id,
            "status": str(refund.status),
            "payment_reference": refund.payment_reference,
            "message": "Refund marked as paid out successfully"
        }
