"""Create Ticket Category Handler"""

from app.application.commands.create_ticket_category_command import (
    CreateTicketCategoryCommand,
)


class CreateTicketCategoryHandler:
    """Handler for CreateTicketCategoryCommand"""

    def __init__(self, ticket_category_repository):
        self.ticket_category_repository = ticket_category_repository

    def handle(self, command: CreateTicketCategoryCommand) -> str:
        """
        Handle ticket category creation
        
        Args:
            command: CreateTicketCategoryCommand instance
            
        Returns:
            Ticket Category ID
        """
        from app.domain.entities.ticket_category import TicketCategory

        ticket_category = TicketCategory(
            event_id=command.event_id,
            name=command.name,
            price=command.price,
            quantity=command.quantity,
            description=command.description,
        )

        self.ticket_category_repository.save(ticket_category)
        return ticket_category.id
