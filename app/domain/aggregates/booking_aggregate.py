from app.domain.entities.ticket import Ticket

from app.domain.events.booking_events import (
    BookingPaid,
    BookingExpired
)


class BookingAggregate:

    def __init__(
        self,
        booking,
        total_price
    ):

        self.booking = booking

        self.total_price = total_price

        self.tickets = []

        self.domain_events = []

    def pay(
        self,
        amount
    ):

        if self.booking.status != "PendingPayment":
            raise ValueError(
                "Booking is not pending payment"
            )

        if (
            self.booking.payment_deadline
            .is_expired()
        ):
            raise ValueError(
                "Payment deadline passed"
            )

        if amount != self.total_price:
            raise ValueError(
                "Incorrect payment amount"
            )

        self.booking.status = "Paid"

        for i in range(
            self.booking.quantity
        ):

            ticket = Ticket(
                f"TICKET-{i+1}"
            )

            self.tickets.append(
                ticket
            )

        self.domain_events.append(
            BookingPaid()
        )

    def expire(self):

        if self.booking.status == "Paid":
            raise ValueError(
                "Paid booking cannot expire"
            )

        self.booking.status = "Expired"

        self.domain_events.append(
            BookingExpired()
        )