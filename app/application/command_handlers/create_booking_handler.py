from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate

class CreateBookingHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        command
    ):

        booking = Booking(
            command.customer_id,
            command.event_id,
            command.ticket_category_name,
            command.quantity
        )

        booking_agg = BookingAggregate(booking)

        self.repository.save(
            booking_agg
        )

        return booking_agg