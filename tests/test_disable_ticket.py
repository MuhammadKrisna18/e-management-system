from datetime import datetime
from app.domain.entities.event import Event
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.entities.ticket_category import TicketCategory

def test_disable_ticket_category_successfully():
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
        50,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)
    aggregate.disable_ticket_category("VIP")

    assert vip_ticket.is_active is False
    assert len(aggregate.domain_events) == 2
    assert type(aggregate.domain_events[1]).__name__ == "TicketCategoryDisabled"
