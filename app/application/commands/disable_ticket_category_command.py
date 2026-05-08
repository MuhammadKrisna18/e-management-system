"""Disable Ticket Category Command"""


class DisableTicketCategoryCommand:
    """Command to disable a ticket category"""

    def __init__(self, ticket_category_id: str):
        self.ticket_category_id = ticket_category_id
