from app.domain.entities.event import Event
from app.domain.aggregates.event_aggregate import EventAggregate


class CreateEventHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        command
    ):

        event = Event(
            command.name,
            command.start_date,
            command.end_date,
            command.capacity
        )

        event_aggregate = EventAggregate(event)

        self.repository.save(
            event_aggregate
        )

        return event_aggregate