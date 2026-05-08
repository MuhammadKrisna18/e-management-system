"""Publish Event Handler"""

from app.application.commands.publish_event_command import PublishEventCommand


class PublishEventHandler:
    """Handler for PublishEventCommand"""

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def handle(self, command: PublishEventCommand) -> None:
        """
        Handle event publishing
        
        Args:
            command: PublishEventCommand instance
        """
        event = self.event_repository.get_by_id(command.event_id)
        event.publish()
        self.event_repository.save(event)
