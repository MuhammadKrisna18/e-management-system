import pytest
from datetime import datetime, timedelta
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)


class TestEventManagementIntegration:

    def setup_method(self):
        self.event_repository = InMemoryEventRepository()

    def test_create_and_publish_event_workflow(self):
        # Create event
        event = Event(
            name="Tech Conference 2026",
            start_date=datetime(2026, 9, 1),
            end_date=datetime(2026, 9, 3),
            capacity=500,
        )
        event.description = "Annual tech conference"
        event.location = "Jakarta Convention Center"

        aggregate = EventAggregate(event)

        # Add ticket categories
        regular_ticket = TicketCategory(
            name="Regular",
            price=1000000.0,
            quota=300,
            sales_start_date=datetime(2026, 7, 1),
            sales_end_date=datetime(2026, 8, 31),
            event_start_date=event.start_date,
        )

        vip_ticket = TicketCategory(
            name="VIP",
            price=2500000.0,
            quota=100,
            sales_start_date=datetime(2026, 7, 1),
            sales_end_date=datetime(2026, 8, 31),
            event_start_date=event.start_date,
        )

        aggregate.add_ticket_category(regular_ticket)
        aggregate.add_ticket_category(vip_ticket)

        # Save event
        event_id = self.event_repository.save(aggregate)

        # Publish event
        saved_aggregate = self.event_repository.get_by_id(event_id)
        saved_aggregate.publish()
        self.event_repository.save(saved_aggregate)

        # Verify
        published_event = self.event_repository.get_by_id(event_id)
        assert published_event.event.status == "Published"
        assert len(published_event.ticket_categories) == 2

    def test_event_cannot_publish_without_ticket_category(self):
        event = Event(
            name="Invalid Event",
            start_date=datetime(2026, 10, 1),
            end_date=datetime(2026, 10, 2),
            capacity=100,
        )

        aggregate = EventAggregate(event)

        with pytest.raises(ValueError):
            aggregate.publish()

    def test_find_published_events(self):
        # Create and publish first event
        event1 = Event(
            name="Event 1",
            start_date=datetime(2026, 9, 1),
            end_date=datetime(2026, 9, 2),
            capacity=100,
        )
        agg1 = EventAggregate(event1)
        ticket1 = TicketCategory(
            "Regular", 100.0, 50,
            datetime(2026, 8, 1), datetime(2026, 8, 31),
            event1.start_date
        )
        agg1.add_ticket_category(ticket1)
        event_id1 = self.event_repository.save(agg1)
        agg1 = self.event_repository.get_by_id(event_id1)
        agg1.publish()
        self.event_repository.save(agg1)

        # Create draft event
        event2 = Event(
            name="Event 2",
            start_date=datetime(2026, 10, 1),
            end_date=datetime(2026, 10, 2),
            capacity=100,
        )
        agg2 = EventAggregate(event2)
        event_id2 = self.event_repository.save(agg2)

        # Find published
        published = self.event_repository.find_published()
        assert len(published) == 1
        assert published[0].event.name == "Event 1"

    def test_cancel_event_disables_all_categories(self):
        event = Event(
            name="Event to Cancel",
            start_date=datetime(2026, 9, 1),
            end_date=datetime(2026, 9, 2),
            capacity=100,
        )
        aggregate = EventAggregate(event)

        ticket1 = TicketCategory(
            "Regular", 100.0, 50,
            datetime(2026, 8, 1), datetime(2026, 8, 31),
            event.start_date
        )
        ticket2 = TicketCategory(
            "VIP", 200.0, 30,
            datetime(2026, 8, 1), datetime(2026, 8, 31),
            event.start_date
        )

        aggregate.add_ticket_category(ticket1)
        aggregate.add_ticket_category(ticket2)

        # Cancel event
        aggregate.cancel()

        # Verify all categories disabled
        for category in aggregate.ticket_categories:
            assert category.is_active is False
        assert aggregate.event.status == "Cancelled"
