from datetime import datetime
from app.domain.events.refund_events import (
    RefundApproved,
    RefundRejected,
    RefundPaidOut
)


class RefundAggregate:

    def __init__(self, refund):
        self.refund = refund
        self.domain_events = []

    def approve_refund(self):
        if self.refund.status != "Requested":
            raise ValueError(
                "Refund must be requested first"
            )

        self.refund.status = "Approved"
        self.refund.approved_at = datetime.now()

        self.domain_events.append(
            RefundApproved(self.refund.refund_id)
        )

    def reject_refund(self, reason: str):
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
            RefundRejected(self.refund.refund_id, reason)
        )

    def mark_as_paid_out(self, payment_reference: str):
        if self.refund.status != "Approved":
            raise ValueError(
                "Refund must be approved first"
            )

        self.refund.status = "PaidOut"
        self.refund.payment_reference = payment_reference
        self.refund.paid_out_at = datetime.now()

        self.domain_events.append(
            RefundPaidOut(self.refund.refund_id, payment_reference)
        )
    
    # Legacy method names for backward compatibility
    def approve(self):
        return self.approve_refund()
    
    def reject(self, reason):
        return self.reject_refund(reason)
    
    def mark_paid_out(self, reference):
        return self.mark_as_paid_out(reference)