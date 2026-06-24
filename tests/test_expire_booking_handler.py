import pytest
from datetime import datetime, timedelta
from app.application.commands.expire_booking_command import ExpireBookingCommand
from app.domain.value_objects.money import Money
from app.application.command_handlers.expire_booking_handler import ExpireBookingHandler
from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.value_objects.booking_status import BookingStatus
from app.infrastructure.repositories.in_memory_booking_repository import InMemoryBookingRepository

def test_expire_booking_success():
    # Setup
    booking_repo = InMemoryBookingRepository()
    money = Money(100.0)
    booking = Booking("CUST001", "EV001", "VIP", 2, money, money)
    # Make payment deadline in the past
    booking.payment_deadline.deadline = datetime.now() - timedelta(hours=1)
    booking_agg = BookingAggregate(booking)
    booking_repo.save(booking_agg)
    booking_id = booking.booking_id

    handler = ExpireBookingHandler(booking_repo)
    command = ExpireBookingCommand(booking_id)

    # Execute
    result_id = handler.handle(command)

    # Verify
    assert result_id == booking_id
    updated_agg = booking_repo.get_by_id(booking_id)
    assert updated_agg.booking.status == BookingStatus.EXPIRED
    
    # Verify event was published (domain events list)
    assert any(type(e).__name__ == "BookingExpired" for e in updated_agg.domain_events)

def test_expire_booking_fails_deadline_not_passed():
    # Setup
    booking_repo = InMemoryBookingRepository()
    money = Money(100.0)
    booking = Booking("CUST001", "EV001", "VIP", 2, money, money)
    # Payment deadline in the future
    booking.payment_deadline.deadline = datetime.now() + timedelta(hours=1)
    booking_agg = BookingAggregate(booking)
    booking_repo.save(booking_agg)
    booking_id = booking.booking_id

    handler = ExpireBookingHandler(booking_repo)
    command = ExpireBookingCommand(booking_id)

    # Execute and Verify
    with pytest.raises(ValueError, match="Cannot expire booking: Payment deadline has not passed"):
        handler.handle(command)

def test_expire_booking_fails_already_paid():
    # Setup
    booking_repo = InMemoryBookingRepository()
    money = Money(100.0)
    booking = Booking("CUST001", "EV001", "VIP", 2, money, money)
    booking.payment_deadline.deadline = datetime.now() - timedelta(hours=1)
    booking.status = BookingStatus.PAID
    booking_agg = BookingAggregate(booking)
    booking_repo.save(booking_agg)
    booking_id = booking.booking_id

    handler = ExpireBookingHandler(booking_repo)
    command = ExpireBookingCommand(booking_id)

    # Execute and Verify
    with pytest.raises(ValueError, match="Can only expire pending bookings"):
        handler.handle(command)
