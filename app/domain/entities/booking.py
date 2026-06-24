from datetime import datetime
from datetime import timedelta

from app.domain.value_objects.payment_deadline import (
    PaymentDeadline
)
from app.domain.value_objects.money import Money


class Booking:

    def __init__(
        self,
        customer_id: str,
        event_id: str,
        ticket_category_name: str,
        quantity: int,
        unit_price: Money,
        total_price: Money
    ):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_name = ticket_category_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
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

    def pay(self, payment_reference: str, amount: Money, paid_at: datetime = None):
        if self.status != "PendingPayment":
            raise ValueError("Can only pay for pending bookings")
        if self.is_payment_deadline_passed():
            raise ValueError("Payment deadline has passed")
        if amount != self.total_price:
            raise ValueError("Payment amount must equal total booking price")
        self.status = "Paid"
        self.payment_reference = payment_reference

    def add_ticket(self, ticket):
        self.tickets.append(ticket)

    def expire(self):
        if self.status != "PendingPayment":
            raise ValueError("Can only expire pending bookings")
        self.status = "Expired"

    def is_payment_deadline_passed(self, current_time: datetime = None) -> bool:
        if current_time is None:
            current_time = datetime.now()
        return current_time > self.payment_deadline.deadline