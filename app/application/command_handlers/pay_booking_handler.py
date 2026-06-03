class PayBookingHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        command
    ):

        aggregate = (
            self.repository.get_by_id(
                command.booking_id
            )
        )

        aggregate.pay(
            command.amount
        )

        self.repository.save(
            aggregate
        )

        return aggregate