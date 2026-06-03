from datetime import datetime
from datetime import timedelta

from app.domain.value_objects.payment_deadline import (
    PaymentDeadline
)


class Booking:

    def __init__(
        self,
        customer_id: str,
        quantity: int
    ):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        self.customer_id = customer_id

        self.quantity = quantity

        self.status = (
            "PendingPayment"
        )

        self.payment_deadline = (
            PaymentDeadline(
                datetime.now()
                + timedelta(
                    minutes=15
                )
            )
        )