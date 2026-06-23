from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.events.event_events import (
    EventPublished,
    EventCancelled,
    TicketCategoryCreated,
    TicketCategoryDisabled
)


class EventAggregate:
    def __init__(self, event: Event):
        self.event = event
        self.ticket_categories = []
        self.domain_events = []

    def add_ticket_category(self, category: TicketCategory):

        if self.event.status == "Completed":
            raise ValueError(
                "Cannot add ticket category to completed event"
            )

        total_quota = sum(
            tc.quota for tc in self.ticket_categories
        )

        if total_quota + category.quota > self.event.capacity:
            raise ValueError(
                "Total quota exceeds event capacity"
            )

        self.ticket_categories.append(category)

        self.domain_events.append(
            TicketCategoryCreated(category.name)
        )
    def publish(self):

        active_categories = [
            category
            for category in self.ticket_categories
            if category.is_active
        ]

        if len(active_categories) == 0:
            raise ValueError(
                "Cannot publish event without active ticket category"
            )

        if self.event.status == "Cancelled":
            raise ValueError(
                "Cancelled event cannot be published"
            )

        self.event.status = "Published"

    def cancel(self):

        if self.event.status == "Completed":
            raise ValueError(
                "Completed event cannot be cancelled"
            )

        self.event.status = "Cancelled"

        for category in self.ticket_categories:
            category.disable()

        self.domain_events.append(
            EventCancelled(self.event.name)
        )

    def disable_ticket_category(self, category_name: str):

        if self.event.status == "Completed":
            raise ValueError(
                "Cannot disable ticket category for completed event"
            )

        for category in self.ticket_categories:

            if category.name == category_name:
                category.disable()
                return

        raise ValueError("Ticket category not found")