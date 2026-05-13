import pytest
from datetime import datetime

from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.aggregates.event_aggregate import EventAggregate


def test_event_invalid_date():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 10),
            datetime(2025, 10, 1),
            100
        )


def test_event_invalid_capacity():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 1),
            datetime(2025, 10, 10),
            0
        )


def test_publish_event_without_ticket_category():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    with pytest.raises(ValueError):
        aggregate.publish()


def test_ticket_category_quota_exceeds_capacity():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        80
    )

    regular_ticket = TicketCategory(
        "Regular",
        100,
        30
    )

    aggregate.add_ticket_category(vip_ticket)

    with pytest.raises(ValueError):
        aggregate.add_ticket_category(regular_ticket)