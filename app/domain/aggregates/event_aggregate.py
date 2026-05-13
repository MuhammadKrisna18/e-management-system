from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory


class EventAggregate:
    def __init__(self, event: Event):
        self.event = event
        self.ticket_categories = []

    def add_ticket_category(self, category: TicketCategory):
        total_quota = sum(tc.quota for tc in self.ticket_categories)

        if total_quota + category.quota > self.event.capacity:
            raise ValueError("Total quota exceeds event capacity")

        self.ticket_categories.append(category)

    def publish(self):
        if len(self.ticket_categories) == 0:
            raise ValueError("Cannot publish event without ticket category")

        self.event.status = "Published"
        
    def cancel(self):
        if self.event.status == "Completed":
            raise ValueError("Completed event cannot be cancelled")
        
        self.event.status = "Cancelled"
        
        for category in self.ticket_categories:
            category.disable()