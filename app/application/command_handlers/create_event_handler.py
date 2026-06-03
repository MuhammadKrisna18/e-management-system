from app.domain.entities.event import Event


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

        self.repository.save(
            event
        )

        return event