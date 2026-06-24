class PayBookingHandler:

    def __init__(
        self,
        repository,
        payment_gateway
    ):
        self.repository = repository
        self.payment_gateway = payment_gateway

    def handle(
        self,
        command
    ):

        aggregate = (
            self.repository.get_by_id(
                command.booking_id
            )
        )

        transaction_id = self.payment_gateway.charge(command.amount)

        aggregate.pay_booking(
            payment_reference=transaction_id
        )

        self.repository.save(
            aggregate
        )

        return aggregate