from app.domain.repositories.refund_repository import RefundRepository
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects.booking_status import BookingStatus


class ApproveRefundHandler:

    def __init__(
        self,
        refund_repository: RefundRepository,
        booking_repository: BookingRepository
    ):
        self.refund_repository = refund_repository
        self.booking_repository = booking_repository

    def handle(self, command) -> dict:
        # Get refund
        refund_agg = self.refund_repository.get_by_id(command.refund_id)
        if not refund_agg:
            raise ValueError(f"Refund {command.refund_id} not found")

        refund = refund_agg.refund

        # Validation: Refund must be in Requested status
        if refund.status != "Requested":
            raise ValueError(
                f"Refund can only be approved if in Requested status. "
                f"Current status: {refund.status}"
            )

        # Approve refund
        refund_agg.approve_refund()

        # Get booking and mark as Refunded
        booking_agg = self.booking_repository.get_by_id(refund.booking_id)
        if booking_agg:
            booking_agg.booking.status = BookingStatus.REFUNDED

            # Cancel all tickets
            if hasattr(booking_agg, 'tickets') and booking_agg.tickets:
                for ticket in booking_agg.tickets:
                    ticket.cancel()

            # Save booking
            self.booking_repository.save(booking_agg)

        # Save refund
        self.refund_repository.save(refund_agg)

        return {
            "refund_id": refund.refund_id,
            "status": str(refund.status),
            "message": "Refund approved successfully"
        }
