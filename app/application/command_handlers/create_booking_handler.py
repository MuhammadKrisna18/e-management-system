from app.domain.entities.booking import Booking


class CreateBookingHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        command
    ):

        booking = Booking(
            command.customer_id,
            command.quantity
        )

        self.repository.save(
            booking
        )

        return booking