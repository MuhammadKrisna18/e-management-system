from datetime import datetime

from app.application.commands.create_event_command import (
    CreateEventCommand
)

from app.application.commands.publish_event_command import (
    PublishEventCommand
)

from app.application.queries.get_available_events_query import (
    GetAvailableEventsQuery
)

from app.application.command_handlers.create_event_handler import (
    CreateEventHandler
)

from app.application.command_handlers.publish_event_handler import (
    PublishEventHandler
)

from app.application.query_handlers.get_available_events_handler import (
    GetAvailableEventsHandler
)

from app.domain.entities.event import Event
from app.domain.entities.ticket_category import (
    TicketCategory
)

from app.domain.aggregates.event_aggregate import (
    EventAggregate
)


# =========================================================
# FAKE REPOSITORIES
# =========================================================

class FakeEventRepository:

    def __init__(
        self,
        aggregate=None
    ):
        self.aggregate = aggregate
        self.saved = None

    def save(
        self,
        obj
    ):
        self.saved = obj

    def get_by_id(
        self,
        event_id
    ):
        return self.aggregate

    def find_published(self):
        if self.aggregate:
            return [self.aggregate]
        return []


# =========================================================
# COMMAND HANDLER TESTS
# =========================================================

def test_create_event_handler():

    repository = (
        FakeEventRepository()
    )

    handler = (
        CreateEventHandler(
            repository
        )
    )

    command = (
        CreateEventCommand(
            "Tech Conference",
            datetime(2026, 1, 1),
            datetime(2026, 1, 2),
            100
        )
    )

    event = handler.handle(
        command
    )

    assert (
        event.event.name
        == "Tech Conference"
    )

    assert (
        repository.saved
        == event
    )


def test_publish_event_handler():

    event = Event(
        "Tech Conference",
        datetime(2026, 1, 1),
        datetime(2026, 1, 2),
        100
    )

    aggregate = EventAggregate(
        event
    )

    category = TicketCategory(
        "Regular",
        100,
        10,
        datetime(2025, 12, 1),
        datetime(2025, 12, 31),
        event.start_date
    )

    aggregate.add_ticket_category(
        category
    )

    repository = (
        FakeEventRepository(
            aggregate
        )
    )

    handler = (
        PublishEventHandler(
            repository
        )
    )

    command = (
        PublishEventCommand(
            "event-1"
        )
    )

    handler.handle(
        command
    )

    assert (
        aggregate.event.status
        == "Published"
    )


# =========================================================
# QUERY HANDLER TESTS
# =========================================================

from app.domain.value_objects.money import Money

def test_get_available_events_handler():
    event = Event("Test Event", datetime(2025, 1, 1), datetime(2025, 1, 2), 100)
    aggregate = EventAggregate(event)
    category = TicketCategory("Regular", 100.0, 10, datetime(2024, 1, 1), datetime(2025, 1, 1), datetime(2025, 1, 1))
    aggregate.add_ticket_category(category)
    
    repository = FakeEventRepository(aggregate)
    handler = GetAvailableEventsHandler(repository)
    result = handler.handle(GetAvailableEventsQuery())

    assert len(result.events) == 1
    assert result.events[0].name == "Test Event"
    assert result.events[0].lowest_ticket_price == 100.0