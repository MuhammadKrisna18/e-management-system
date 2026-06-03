from app.domain.events.refund_events import (
    RefundApproved,
    RefundRejected,
    RefundPaidOut
)


class RefundAggregate:

    def __init__(
        self,
        refund
    ):

        self.refund = refund

        self.domain_events = []

    def approve(self):

        if (
            self.refund.status
            != "Requested"
        ):
            raise ValueError(
                "Refund must be requested first"
            )

        self.refund.status = (
            "Approved"
        )

        self.domain_events.append(
            RefundApproved()
        )

    def reject(
        self,
        reason
    ):

        if (
            self.refund.status
            != "Requested"
        ):
            raise ValueError(
                "Refund must be requested first"
            )

        if not reason:
            raise ValueError(
                "Reason required"
            )

        self.refund.status = (
            "Rejected"
        )

        self.refund.rejection_reason = (
            reason
        )

        self.domain_events.append(
            RefundRejected()
        )

    def mark_paid_out(
        self,
        reference
    ):

        if (
            self.refund.status
            != "Approved"
        ):
            raise ValueError(
                "Refund must be approved"
            )

        self.refund.status = (
            "PaidOut"
        )

        self.refund.payment_reference = (
            reference
        )

        self.domain_events.append(
            RefundPaidOut()
        )