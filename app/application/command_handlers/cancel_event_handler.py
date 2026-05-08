"""Cancel Event Handler"""

from app.application.commands.cancel_event_command import CancelEventCommand


class CancelEventHandler:
    """Handler for CancelEventCommand"""

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def handle(self, command: CancelEventCommand) -> None:
        """
        Handle event cancellation
        
        Args:
            command: CancelEventCommand instance
        """
        event = self.event_repository.get_by_id(command.event_id)
        event.cancel(reason=command.reason)
        self.event_repository.save(event)
