"""Booking Aggregate - Coordinates Booking and Tickets"""
from datetime import datetime
from app.domain.entities.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.events.booking_events import (
    BookingPaid,
    BookingExpired,
    TicketReserved
)


class BookingAggregate:
    """
    Aggregate for booking - coordinates Booking and Tickets.
    Manages the lifecycle of bookings and associated tickets.
    """

    def __init__(self, booking: Booking):
        """
        Initialize booking aggregate.
        
        Args:
            booking: Booking entity (aggregate root)
        """
        self.booking = booking
        self.domain_events = []

    def create_tickets(self):
        """
        Create tickets for the booking.
        Generates unique ticket codes and creates Ticket entities.
        
        Raises:
            ValueError: If tickets already created
        """
        if len(self.booking.tickets) > 0:
            raise ValueError("Tickets already created for this booking")

        for i in range(self.booking.quantity):
            ticket_code = TicketCode()
            ticket = Ticket(
                ticket_code=ticket_code
            )
            self.booking.add_ticket(ticket)

        self.domain_events.append(
            TicketReserved(
                booking_id=self.booking.booking_id,
                event_id=self.booking.event_id,
                ticket_category=self.booking.ticket_category_name,
                quantity=self.booking.quantity,
                total_price=self.booking.total_price,
            )
        )

    def pay_booking(self, payment_reference: str, paid_at: datetime = None):
        """
        Process booking payment.
        Marks booking as PAID and raises BookingPaid event.
        
        Args:
            payment_reference: Payment transaction reference
            paid_at: Payment timestamp (optional)
        """
        self.booking.pay(payment_reference, paid_at)

        self.domain_events.append(
            BookingPaid(
                booking_id=self.booking.booking_id,
                amount=self.booking.total_price,
                payment_reference=payment_reference,
            )
        )

    def expire_booking(self):
        """
        Expire the booking and release ticket quota.
        Marks booking as EXPIRED and raises BookingExpired event.
        """
        self.booking.expire()

        self.domain_events.append(
            BookingExpired(
                booking_id=self.booking.booking_id,
            )
        )

    def get_domain_events(self):
        """
        Get all domain events for publishing.
        
        Returns:
            List of domain events
        """
        return self.domain_events

    def clear_domain_events(self):
        """Clear domain events after publishing."""
        self.domain_events = []
