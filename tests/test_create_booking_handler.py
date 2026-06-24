from datetime import datetime
from app.application.commands.create_booking_command import CreateBookingCommand
from app.application.command_handlers.create_booking_handler import CreateBookingHandler
from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.aggregates.event_aggregate import EventAggregate

class FakeBookingRepository:
    def __init__(self):
        self.saved = None

    def save(self, obj):
        self.saved = obj

class FakeEventRepositoryForBooking:
    def __init__(self, aggregate):
        self.aggregate = aggregate

    def get_by_id(self, event_id):
        return self.aggregate

def test_create_booking_handler_calculates_total_price():
    event = Event(
        "Tech Conference",
        datetime(2026, 1, 1),
        datetime(2026, 1, 2),
        100
    )
    event.event_id = "EV001"
    aggregate = EventAggregate(event)
    category = TicketCategory(
        "VIP",
        150.0,
        10,
        datetime(2025, 12, 1),
        datetime(2025, 12, 31),
        event.start_date
    )
    aggregate.add_ticket_category(category)

    event_repo = FakeEventRepositoryForBooking(aggregate)
    booking_repo = FakeBookingRepository()

    handler = CreateBookingHandler(booking_repo, event_repo)
    command = CreateBookingCommand(
        "CUST001",
        "EV001",
        "VIP",
        3
    )

    booking_agg = handler.handle(command)

    assert booking_agg.booking.unit_price == 150.0
    assert booking_agg.booking.total_price == 450.0
    assert booking_repo.saved == booking_agg
