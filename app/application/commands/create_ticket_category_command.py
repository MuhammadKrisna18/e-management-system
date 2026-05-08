"""Create Ticket Category Command"""

from decimal import Decimal


class CreateTicketCategoryCommand:
    """Command to create a new ticket category"""

    def __init__(
        self,
        event_id: str,
        name: str,
        price: Decimal,
        quantity: int,
        description: str = "",
    ):
        self.event_id = event_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
