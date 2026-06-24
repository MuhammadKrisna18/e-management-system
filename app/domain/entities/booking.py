from datetime import datetime
from datetime import timedelta

from app.domain.value_objects.payment_deadline import (
    PaymentDeadline
)


class Booking:

    def __init__(
        self,
        customer_id: str,
        event_id: str,
        ticket_category_name: str,
        quantity: int
    ):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_name = ticket_category_name
        self.quantity = quantity
        self.total_price = 0.0 # Will be calculated later
        self.booking_id = None
        self.tickets = []

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

    def pay(self, payment_reference: str, paid_at: datetime = None):
        if self.status != "PendingPayment":
            raise ValueError("Can only pay for pending bookings")
        self.status = "Paid"
        self.payment_reference = payment_reference

    def add_ticket(self, ticket):
        self.tickets.append(ticket)

    def expire(self):
        if self.status != "PendingPayment":
            raise ValueError("Can only expire pending bookings")
        self.status = "Expired"