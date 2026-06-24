from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate

class CreateBookingHandler:

    def __init__(
        self,
        repository,
        event_repository
    ):
        self.repository = repository
        self.event_repository = event_repository

    def handle(
        self,
        command
    ):

        event_agg = self.event_repository.get_by_id(command.event_id)
        if not event_agg:
            raise ValueError(f"Event {command.event_id} not found")

        ticket_category = None
        for category in event_agg.ticket_categories:
            if category.name == command.ticket_category_name:
                ticket_category = category
                break

        if not ticket_category:
            raise ValueError(f"Ticket category {command.ticket_category_name} not found in event {command.event_id}")

        if not ticket_category.is_active:
            raise ValueError(f"Ticket category {command.ticket_category_name} is disabled")

        unit_price = ticket_category.price
        total_price = unit_price * command.quantity

        booking = Booking(
            command.customer_id,
            command.event_id,
            command.ticket_category_name,
            command.quantity,
            unit_price,
            total_price
        )

        booking_agg = BookingAggregate(booking)

        self.repository.save(
            booking_agg
        )

        return booking_agg