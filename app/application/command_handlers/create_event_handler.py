"""Create Event Handler"""

from app.application.commands.create_event_command import CreateEventCommand
from app.domain.aggregates.event_aggregate import EventAggregate


class CreateEventHandler:
    """Handler for CreateEventCommand"""

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> str:
        """
        Handle event creation
        
        Args:
            command: CreateEventCommand instance
            
        Returns:
            Event ID
        """
        event = EventAggregate(
            name=command.name,
            description=command.description,
            location=command.location,
            start_date=command.start_date,
            end_date=command.end_date,
            organizer_id=command.organizer_id,
            max_capacity=command.max_capacity,
            status=command.status,
        )
        
        self.event_repository.save(event)
        return event.id
