from datetime import datetime
from app.domain.entities.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.money import Money
from app.domain.events.booking_events import (
    BookingPaid,
    BookingExpired,
    TicketReserved
)


class BookingAggregate:

    def __init__(self, booking: Booking):
        self.booking = booking
        self.domain_events = [
            TicketReserved(
                booking_id=self.booking.booking_id,
                event_id=self.booking.event_id,
                ticket_category=self.booking.ticket_category_name,
                quantity=self.booking.quantity,
                total_price=self.booking.total_price.amount if hasattr(self.booking.total_price, 'amount') else self.booking.total_price,
            )
        ]

    def create_tickets(self):
        if len(self.booking.tickets) > 0:
            raise ValueError("Tickets already created for this booking")

        for i in range(self.booking.quantity):
            ticket_code = TicketCode()
            ticket = Ticket(
                ticket_code=ticket_code,
                event_id=self.booking.event_id
            )
            self.booking.add_ticket(ticket)

    def pay_booking(self, payment_reference: str, amount: 'Money', paid_at: datetime = None):
        self.booking.pay(payment_reference, amount, paid_at)
        
        # Issue tickets after payment
        self.create_tickets()

        self.domain_events.append(
            BookingPaid(
                booking_id=self.booking.booking_id,
                amount=self.booking.total_price.amount if hasattr(self.booking.total_price, 'amount') else self.booking.total_price,
                payment_reference=payment_reference,
            )
        )

    def expire_booking(self):
        self.booking.expire()

        self.domain_events.append(
            BookingExpired(
                booking_id=self.booking.booking_id,
            )
        )

    def get_domain_events(self):
        return self.domain_events

    def clear_domain_events(self):
        self.domain_events = []
