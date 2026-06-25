import uuid
from datetime import datetime, timedelta
from app.domain.entities.refund import Refund
from app.domain.aggregates.refund_aggregate import RefundAggregate
from app.domain.value_objects.money import Money
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.refund_repository import RefundRepository


class RequestRefundHandler:

    def __init__(
        self,
        booking_repository: BookingRepository,
        refund_repository: RefundRepository
    ):
        self.booking_repository = booking_repository
        self.refund_repository = refund_repository

    def handle(self, command) -> str:
        # Get booking
        booking_agg = self.booking_repository.get_by_id(command.booking_id)
        if not booking_agg:
            raise ValueError(f"Booking {command.booking_id} not found")

        booking = booking_agg.booking

        # Validation: Booking must be Paid
        if booking.status != "Paid":
            raise ValueError(
                f"Refund can only be requested for paid bookings. "
                f"Current status: {booking.status}"
            )

        # Validation: Check if any ticket has been checked in
        if hasattr(booking, 'tickets') and booking.tickets:
            for ticket in booking.tickets:
                if ticket.status == "CheckedIn":
                    raise ValueError(
                        "Refund cannot be requested if ticket has already been checked in"
                    )

        # Validation: Check refund deadline
        refund_deadline = datetime.now() + timedelta(days=7)
        if datetime.now() > refund_deadline:
            raise ValueError("Refund deadline has passed")

        # Create refund
        refund_id = str(uuid.uuid4())
        refund = Refund(
            refund_id=refund_id,
            booking_id=booking.booking_id,
            customer_id=booking.customer_id,
            event_id=booking.event_id,
            refund_amount=booking.total_price,  # Assuming booking has total_price
            refund_deadline=refund_deadline,
            reason=command.reason,
        )

        # Create aggregate
        refund_agg = RefundAggregate(refund)

        # Save refund
        self.refund_repository.save(refund_agg)

        return refund_id
