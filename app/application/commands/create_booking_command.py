class CreateBookingCommand:

    def __init__(
        self,
        customer_id,
        event_id,
        ticket_category_name,
        quantity
    ):
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_name = ticket_category_name
        self.quantity = quantity