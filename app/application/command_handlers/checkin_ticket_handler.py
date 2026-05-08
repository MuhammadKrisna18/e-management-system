"""Check-in Ticket Handler"""

from app.application.commands.checkin_ticket_command import CheckinTicketCommand


class CheckinTicketHandler:
    """Handler for CheckinTicketCommand"""

    def __init__(self, ticket_repository):
        self.ticket_repository = ticket_repository

    def handle(self, command: CheckinTicketCommand) -> None:
        """
        Handle ticket check-in
        
        Args:
            command: CheckinTicketCommand instance
        """
        ticket = self.ticket_repository.get_by_id(command.ticket_id)
        ticket.checkin(location=command.location, checked_in_at=command.checked_in_at)
        self.ticket_repository.save(ticket)
