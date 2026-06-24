from app.domain.repositories.refund_repository import RefundRepository


class RejectRefundHandler:

    def __init__(self, refund_repository: RefundRepository):
        self.refund_repository = refund_repository

    def handle(self, command) -> dict:
        # Get refund
        refund_agg = self.refund_repository.get_by_id(command.refund_id)
        if not refund_agg:
            raise ValueError(f"Refund {command.refund_id} not found")

        refund = refund_agg.refund

        # Validation: Refund must be in Requested status
        if refund.status != "Requested":
            raise ValueError(
                f"Refund can only be rejected if in Requested status. "
                f"Current status: {refund.status}"
            )

        # Validation: Reason must be provided
        if not hasattr(command, 'reason') or not command.reason:
            raise ValueError("Rejection reason must be provided")

        # Reject refund
        refund_agg.reject_refund(command.reason)

        # Save refund
        self.refund_repository.save(refund_agg)

        return {
            "refund_id": refund.refund_id,
            "status": str(refund.status),
            "reason": refund.rejection_reason,
            "message": "Refund rejected successfully"
        }
