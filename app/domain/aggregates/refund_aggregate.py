"""Refund Aggregate Root"""
from datetime import datetime
from app.domain.events.refund_events import (
    RefundApproved,
    RefundRejected,
    RefundPaidOut
)


class RefundAggregate:
    """
    Aggregate root for refund operations.
    
    Manages the lifecycle of a refund from request to payout.
    Enforces business rules around refund state transitions.
    """

    def __init__(self, refund):
        """
        Initialize refund aggregate.
        
        Args:
            refund: Refund entity
        """
        self.refund = refund
        self.domain_events = []

    def approve_refund(self):
        """
        Approve the refund request.
        
        Raises:
            ValueError: If refund is not in Requested status
        """
        if self.refund.status != "Requested":
            raise ValueError(
                "Refund must be requested first"
            )

        self.refund.status = "Approved"
        self.refund.approved_at = datetime.now()

        self.domain_events.append(
            RefundApproved()
        )

    def reject_refund(self, reason: str):
        """
        Reject the refund request.
        
        Args:
            reason: Reason for rejection
            
        Raises:
            ValueError: If refund is not in Requested status or reason missing
        """
        if self.refund.status != "Requested":
            raise ValueError(
                "Refund must be requested first"
            )

        if not reason:
            raise ValueError(
                "Reason required"
            )

        self.refund.status = "Rejected"
        self.refund.rejection_reason = reason
        self.refund.rejected_at = datetime.now()

        self.domain_events.append(
            RefundRejected()
        )

    def mark_as_paid_out(self, payment_reference: str):
        """
        Mark refund as paid out.
        
        Args:
            payment_reference: Reference ID from payment service
            
        Raises:
            ValueError: If refund is not in Approved status
        """
        if self.refund.status != "Approved":
            raise ValueError(
                "Refund must be approved first"
            )

        self.refund.status = "PaidOut"
        self.refund.payment_reference = payment_reference
        self.refund.paid_out_at = datetime.now()

        self.domain_events.append(
            RefundPaidOut()
        )
    
    # Legacy method names for backward compatibility
    def approve(self):
        """Legacy method name - use approve_refund() instead"""
        return self.approve_refund()
    
    def reject(self, reason):
        """Legacy method name - use reject_refund() instead"""
        return self.reject_refund(reason)
    
    def mark_paid_out(self, reference):
        """Legacy method name - use mark_as_paid_out() instead"""
        return self.mark_as_paid_out(reference)