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

    def get_booked_quantity_for_category(self, event_id: str, ticket_category_name: str) -> int:
        return 0

    def find_active_by_customer_and_event(self, customer_id: str, event_id: str):
        return []

class FakeEventRepositoryForBooking:
    def __init__(self, aggregate):
        self.aggregate = aggregate

    def get_by_id(self, event_id):
        return self.aggregate

def test_create_booking_handler_calculates_total_price():
    event = Event(
        "Tech Conference",
        datetime(2026, 12, 1),
        datetime(2026, 12, 2),
        100
    )
    event.event_id = "EV001"
    aggregate = EventAggregate(event)
    category = TicketCategory(
        "VIP",
        150.0,
        10,
        datetime(2026, 1, 1),
        datetime(2026, 11, 30),
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

    assert booking_agg.booking.unit_price.amount == 150.0
    assert booking_agg.booking.total_price.amount == 450.0
    assert booking_repo.saved == booking_agg

def test_create_booking_fails_out_of_sales_period():
    event = Event("Tech", datetime(2026, 12, 1), datetime(2026, 12, 2), 100)
    event.event_id = "EV001"
    aggregate = EventAggregate(event)
    category = TicketCategory(
        "VIP", 150.0, 10,
        datetime(2025, 1, 1), # Sales ended in 2025
        datetime(2025, 12, 31),
        event.start_date
    )
    aggregate.add_ticket_category(category)

    event_repo = FakeEventRepositoryForBooking(aggregate)
    booking_repo = FakeBookingRepository()

    handler = CreateBookingHandler(booking_repo, event_repo)
    command = CreateBookingCommand("CUST001", "EV001", "VIP", 3)

    import pytest
    with pytest.raises(ValueError, match="Booking is only allowed within the ticket sales period"):
        handler.handle(command)

def test_create_booking_fails_exceeding_quota():
    event = Event("Tech", datetime(2026, 12, 1), datetime(2026, 12, 2), 100)
    event.event_id = "EV001"
    aggregate = EventAggregate(event)
    category = TicketCategory(
        "VIP", 150.0, 5, # Only 5 quota
        datetime(2026, 1, 1),
        datetime(2026, 11, 30),
        event.start_date
    )
    aggregate.add_ticket_category(category)

    event_repo = FakeEventRepositoryForBooking(aggregate)
    booking_repo = FakeBookingRepository()
    booking_repo.get_booked_quantity_for_category = lambda e, c: 3 # 3 already booked

    handler = CreateBookingHandler(booking_repo, event_repo)
    command = CreateBookingCommand("CUST001", "EV001", "VIP", 3) # requesting 3, remaining is 2

    import pytest
    with pytest.raises(ValueError, match="Requested quantity exceeds remaining ticket quota"):
        handler.handle(command)

def test_create_booking_fails_duplicate_active_booking():
    event = Event("Tech", datetime(2026, 12, 1), datetime(2026, 12, 2), 100)
    event.event_id = "EV001"
    aggregate = EventAggregate(event)
    category = TicketCategory(
        "VIP", 150.0, 10,
        datetime(2026, 1, 1),
        datetime(2026, 11, 30),
        event.start_date
    )
    aggregate.add_ticket_category(category)

    event_repo = FakeEventRepositoryForBooking(aggregate)
    booking_repo = FakeBookingRepository()
    # Mock returning an active booking
    booking_repo.find_active_by_customer_and_event = lambda c, e: [object()]

    handler = CreateBookingHandler(booking_repo, event_repo)
    command = CreateBookingCommand("CUST001", "EV001", "VIP", 3)

    import pytest
    with pytest.raises(ValueError, match="Customer already has an active booking for this event"):
        handler.handle(command)
