class CreateBookingCommand:

    def __init__(
        self,
        customer_id,
        quantity
    ):
        self.customer_id = customer_id
        self.quantity = quantity