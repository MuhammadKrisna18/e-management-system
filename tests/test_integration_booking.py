"""Integration Tests for Booking Workflow"""
import pytest
import uuid
from datetime import datetime, timedelta
from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_code import TicketCode
from app.infrastructure.repositories.in_memory_booking_repository import (
    InMemoryBookingRepository,
)
from app.infrastructure.repositories.in_memory_ticket_repository import (
    InMemoryTicketRepository,
)


class TestBookingWorkflowIntegration:
    """Integration tests for complete booking workflow."""

    def setup_method(self):
        """Setup test fixtures."""
        self.booking_repository = InMemoryBookingRepository()
        self.ticket_repository = InMemoryTicketRepository()

    def test_complete_booking_to_payment_workflow(self):
        """Test complete workflow from booking creation to payment."""
        # Create booking
        booking_id = str(uuid.uuid4())
        booking = Booking(
            customer_id="CUST001",
            event_id="EV001",
            ticket_category_name="VIP",
            quantity=2,
            unit_price=Money(500000.0),
            total_price=Money(1000000.0),
        )
        booking.booking_id = booking_id

        booking_agg = BookingAggregate(booking)
        self.booking_repository.save(booking_agg)

        # Verify booking created without tickets
        saved_booking = self.booking_repository.get_by_id(booking_id)
        assert saved_booking.booking.status == "PendingPayment"
        assert len(saved_booking.booking.tickets) == 0

        # Pay booking
        payment_ref = "TXN123456"
        saved_booking.pay_booking(payment_ref, Money(1000000.0))
        self.booking_repository.save(saved_booking)

        # Verify payment
        paid_booking = self.booking_repository.get_by_id(booking_id)
        assert paid_booking.booking.status == "Paid"
        assert paid_booking.booking.payment_reference == payment_ref
        assert len(paid_booking.booking.tickets) == 2

    def test_expired_booking_workflow(self):
        """Test booking expiration workflow."""
        # Create booking with short deadline
        booking_id = str(uuid.uuid4())
        created_at = datetime.now() - timedelta(minutes=20)
        booking = Booking(
            customer_id="CUST001",
            event_id="EV001",
            ticket_category_name="Regular",
            quantity=1,
            unit_price=Money(100000.0),
            total_price=Money(100000.0),
        )
        booking.booking_id = booking_id
        # Manually adjust deadline for expiration
        booking.payment_deadline.deadline = created_at + timedelta(minutes=15)

        booking_agg = BookingAggregate(booking)
        self.booking_repository.save(booking_agg)

        # Expire booking
        saved_booking = self.booking_repository.get_by_id(booking_id)
        assert saved_booking.booking.is_payment_deadline_passed() is True

        saved_booking.expire_booking()
        self.booking_repository.save(saved_booking)

        # Verify expiration
        expired_booking = self.booking_repository.get_by_id(booking_id)
        assert expired_booking.booking.status == "Expired"

    def test_find_expired_pending_bookings(self):
        """Test finding expired pending bookings."""
        # Create expired booking
        expired_id = str(uuid.uuid4())
        created_at = datetime.now() - timedelta(minutes=20)
        expired_booking = Booking(
            customer_id="CUST001",
            event_id="EV001",
            ticket_category_name="Regular",
            quantity=1,
            unit_price=Money(100.0),
            total_price=Money(100.0),
        )
        expired_booking.booking_id = expired_id
        expired_booking.payment_deadline.deadline = created_at + timedelta(minutes=15)
        expired_agg = BookingAggregate(expired_booking)
        self.booking_repository.save(expired_agg)

        # Create active booking
        active_id = str(uuid.uuid4())
        active_booking = Booking(
            customer_id="CUST002",
            event_id="EV002",
            ticket_category_name="VIP",
            quantity=2,
            unit_price=Money(200.0),
            total_price=Money(400.0),
        )
        active_booking.booking_id = active_id
        active_agg = BookingAggregate(active_booking)
        self.booking_repository.save(active_agg)

        # Find expired
        expired = self.booking_repository.find_expired_pending()
        assert len(expired) == 1
        assert expired[0].booking.booking_id == expired_id

    def test_ticket_check_in_workflow(self):
        """Test ticket check-in workflow."""
        # Create booking with tickets
        booking_id = str(uuid.uuid4())
        booking = Booking(
            customer_id="CUST001",
            event_id="EV001",
            ticket_category_name="VIP",
            quantity=1,
            unit_price=Money(500000.0),
            total_price=Money(500000.0),
        )
        booking.booking_id = booking_id

        booking_agg = BookingAggregate(booking)
        booking_agg.pay_booking("REF_CHK", Money(500000.0))

        # Save tickets
        for ticket in booking_agg.booking.tickets:
            self.ticket_repository.save(ticket)
            ticket_code = ticket.ticket_code.value

        # Check in ticket
        ticket = self.ticket_repository.find_by_code(ticket_code)
        ticket.check_in()
        self.ticket_repository.save(ticket)

        # Verify check-in
        checked_in_ticket = self.ticket_repository.find_by_code(ticket_code)
        assert checked_in_ticket.status.value == "CheckedIn"
        assert checked_in_ticket.checked_in_at is not None
