"""Reject Refund Command Handler"""
from app.domain.repositories.refund_repository import RefundRepository


class RejectRefundHandler:
    """
    Handler for RejectRefundCommand.
    Implements User Story 17: Reject Refund
    
    An Event Organizer can reject a refund request with a reason.
    When rejected, the refund status changes to Rejected and related 
    booking remains Paid with tickets remaining Active.
    """

    def __init__(self, refund_repository: RefundRepository):
        """
        Initialize handler with refund repository.
        
        Args:
            refund_repository: RefundRepository instance
        """
        self.refund_repository = refund_repository

    def handle(self, command) -> dict:
        """
        Handle RejectRefundCommand.
        
        Args:
            command: RejectRefundCommand with refund_id and reason
            
        Returns:
            dict: Result with refund_id and status
            
        Raises:
            ValueError: If refund not found, not in Requested status,
                       or reason missing
        """
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
