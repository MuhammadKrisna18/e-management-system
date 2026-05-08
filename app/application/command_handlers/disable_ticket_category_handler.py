"""Disable Ticket Category Handler"""

from app.application.commands.disable_ticket_category_command import (
    DisableTicketCategoryCommand,
)


class DisableTicketCategoryHandler:
    """Handler for DisableTicketCategoryCommand"""

    def __init__(self, ticket_category_repository):
        self.ticket_category_repository = ticket_category_repository

    def handle(self, command: DisableTicketCategoryCommand) -> None:
        """
        Handle ticket category disabling
        
        Args:
            command: DisableTicketCategoryCommand instance
        """
        ticket_category = self.ticket_category_repository.get_by_id(
            command.ticket_category_id
        )
        ticket_category.disable()
        self.ticket_category_repository.save(ticket_category)
