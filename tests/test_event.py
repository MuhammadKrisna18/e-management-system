import pytest
from datetime import datetime

from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.services.pricing_service import PricingService
from app.domain.value_objects.money import Money

from datetime import datetime, timedelta

from app.domain.entities.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.refund_status import (
    RefundStatus
)
from app.domain.value_objects.money import Money
from app.domain.entities.refund import Refund

from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.aggregates.refund_aggregate import RefundAggregate


# =========================================================
# EVENT TESTS
# =========================================================

def test_event_invalid_date():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 10),
            datetime(2025, 10, 1),
            100
        )


def test_event_invalid_capacity_zero():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 1),
            datetime(2025, 10, 10),
            0
        )


def test_event_invalid_capacity_negative():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 1),
            datetime(2025, 10, 10),
            -10
        )


def test_event_default_status_is_draft():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    assert event.status == "Draft"


# =========================================================
# TICKET CATEGORY TESTS
# =========================================================

def test_ticket_price_cannot_be_negative():
    with pytest.raises(ValueError):
        TicketCategory(
            "VIP",
            -100,
            10,
            datetime(2025, 9, 1),
            datetime(2025, 9, 20),
            datetime(2025, 10, 1)
        )


def test_ticket_quota_must_be_greater_than_zero():
    with pytest.raises(ValueError):
        TicketCategory(
            "VIP",
            100,
            0,
            datetime(2025, 9, 1),
            datetime(2025, 9, 20),
            datetime(2025, 10, 1)
        )


def test_disable_ticket_category():
    ticket = TicketCategory(
        "VIP",
        100,
        10,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        datetime(2025, 10, 1)
    )

    ticket.disable()

    assert ticket.is_active is False


def test_ticket_sales_period_invalid():

    event = Event(
        "Music Festival",
        datetime(2025, 10, 10),
        datetime(2025, 10, 12),
        100
    )

    with pytest.raises(ValueError):

        TicketCategory(
            "VIP",
            500,
            10,
            datetime(2025, 10, 1),
            datetime(2025, 10, 11),
            event.start_date
        )


# =========================================================
# EVENT AGGREGATE TESTS
# =========================================================

def test_publish_event_without_ticket_category():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    with pytest.raises(ValueError):
        aggregate.publish()


def test_publish_event_successfully():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        50,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)

    aggregate.publish()

    assert event.status == "Published"


def test_ticket_category_quota_exceeds_capacity():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        80,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        event.start_date
    )

    regular_ticket = TicketCategory(
        "Regular",
        100,
        30,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)

    with pytest.raises(ValueError):
        aggregate.add_ticket_category(regular_ticket)


def test_cancel_event_successfully():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        50,
        datetime(2025, 9, 1),
        datetime(2025, 9, 20),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)

    aggregate.cancel()

    assert event.status == "Cancelled"
    assert vip_ticket.is_active is False


def test_completed_event_cannot_be_cancelled():
    event = Event(
        "Music Festival",
        datetime(2025, 10, 1),
        datetime(2025, 10, 2),
        100
    )

    event.status = "Completed"

    aggregate = EventAggregate(event)

    with pytest.raises(ValueError):
        aggregate.cancel()


def test_cancelled_event_cannot_be_published():

    event = Event(
        "Music Festival",
        datetime(2025, 10, 10),
        datetime(2025, 10, 12),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        10,
        datetime(2025, 10, 1),
        datetime(2025, 10, 5),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)

    aggregate.cancel()

    with pytest.raises(ValueError):
        aggregate.publish()


def test_disable_ticket_category_successfully():

    event = Event(
        "Music Festival",
        datetime(2025, 10, 10),
        datetime(2025, 10, 12),
        100
    )

    aggregate = EventAggregate(event)

    vip_ticket = TicketCategory(
        "VIP",
        500,
        10,
        datetime(2025, 10, 1),
        datetime(2025, 10, 5),
        event.start_date
    )

    aggregate.add_ticket_category(vip_ticket)

    aggregate.disable_ticket_category("VIP")

    assert vip_ticket.is_active is False


def test_completed_event_cannot_disable_ticket_category():

    event = Event(
        "Music Festival",
        datetime(2025, 10, 10),
        datetime(2025, 10, 12),
        100
    )

    event.status = "Completed"

    aggregate = EventAggregate(event)

    with pytest.raises(ValueError):

        aggregate.disable_ticket_category("VIP")


# =========================================================
# MONEY VALUE OBJECT TESTS
# =========================================================

def test_money_cannot_be_negative():
    with pytest.raises(ValueError):
        Money(-100)


def test_money_addition():
    money1 = Money(100)
    money2 = Money(50)

    result = money1.add(money2)

    assert result.amount == 150


# =========================================================
# PRICING SERVICE TESTS
# =========================================================

def test_calculate_total_price_without_service_fee():
    result = PricingService.calculate_total_price(
        ticket_price=100,
        quantity=2
    )

    assert result.amount == 200


def test_calculate_total_price_with_service_fee():
    result = PricingService.calculate_total_price(
        ticket_price=100,
        quantity=2,
        service_fee=20
    )

    assert result.amount == 220


def test_quantity_must_be_greater_than_zero():
    with pytest.raises(ValueError):
        PricingService.calculate_total_price(
            ticket_price=100,
            quantity=0
        )
        
        

# =========================================================
# BOOKING TESTS
# =========================================================

def test_booking_quantity_must_be_positive():

    with pytest.raises(ValueError):

        Booking(
            customer_id="customer-1",
            event_id="EV001",
            ticket_category_name="VIP",
            quantity=0,
            unit_price=Money(100.0),
            total_price=Money(0.0)
        )


def test_booking_cannot_pay_after_deadline():

    booking = Booking(
        customer_id="customer-1",
        event_id="EV001",
        ticket_category_name="VIP",
        quantity=1,
        unit_price=100.0,
        total_price=100.0
    )

    booking.payment_deadline.deadline = (
        datetime.now()
        - timedelta(minutes=1)
    )

    aggregate = BookingAggregate(
        booking
    )

    with pytest.raises(ValueError):
        aggregate.pay_booking("REF123", Money(100.0))





def test_paid_booking_cannot_expire():

    booking = Booking(
        customer_id="customer-1",
        event_id="EV001",
        ticket_category_name="VIP",
        quantity=1,
        unit_price=Money(100.0),
        total_price=Money(100.0)
    )

    aggregate = BookingAggregate(
        booking
    )

    aggregate.pay_booking("REF123", Money(100.0))

    with pytest.raises(ValueError):
        aggregate.expire_booking()


# =========================================================
# TICKET TESTS
# =========================================================

from app.domain.exceptions import TicketAlreadyCheckedException

def test_ticket_cannot_checkin_twice():

    ticket = Ticket(
        ticket_code=TicketCode(),
        event_id="EV001"
    )

    ticket.check_in()

    with pytest.raises(TicketAlreadyCheckedException):
        ticket.check_in()


# =========================================================
# REFUND TESTS
# =========================================================

def test_refund_cannot_approve_if_not_requested():

    refund = Refund(
        refund_id="REF001",
        booking_id="BKG001",
        customer_id="CUST001",
        event_id="EV001",
        refund_amount=100.0,
        refund_deadline=datetime.now()
    )

    aggregate = RefundAggregate(
        refund
    )

    aggregate.approve()

    with pytest.raises(ValueError):
        aggregate.approve()


def test_rejected_refund_must_have_reason():

    refund = Refund(
        refund_id="REF001",
        booking_id="BKG001",
        customer_id="CUST001",
        event_id="EV001",
        refund_amount=100.0,
        refund_deadline=datetime.now()
    )

    aggregate = RefundAggregate(
        refund
    )

    with pytest.raises(ValueError):
        aggregate.reject("")


def test_refund_mark_paid_out_requires_approved_status():

    refund = Refund(
        refund_id="REF001",
        booking_id="BKG001",
        customer_id="CUST001",
        event_id="EV001",
        refund_amount=100.0,
        refund_deadline=datetime.now()
    )

    aggregate = RefundAggregate(
        refund
    )

    with pytest.raises(ValueError):

        aggregate.mark_paid_out(
            "REF123"
        )

def test_booking_cannot_pay_with_incorrect_payment_amount():
    booking = Booking(
        customer_id="customer-1",
        event_id="EV001",
        ticket_category_name="VIP",
        quantity=1,
        unit_price=Money(100.0),
        total_price=Money(100.0)
    )
    aggregate = BookingAggregate(booking)
    
    with pytest.raises(ValueError):
        aggregate.pay_booking("REF123", Money(50.0))

def test_refund_cannot_be_requested_if_ticket_has_already_been_checked_in():
    from app.application.command_handlers.request_refund_handler import RequestRefundHandler
    from app.application.commands.request_refund_command import RequestRefundCommand
    from app.infrastructure.repositories.in_memory_booking_repository import InMemoryBookingRepository
    from app.infrastructure.repositories.in_memory_refund_repository import InMemoryRefundRepository
    from app.domain.entities.ticket import Ticket
    from app.domain.value_objects.ticket_code import TicketCode
    from app.domain.constants import TicketStatuses

    booking_repo = InMemoryBookingRepository()
    refund_repo = InMemoryRefundRepository()

    booking = Booking(
        customer_id="customer-1",
        event_id="EV001",
        ticket_category_name="VIP",
        quantity=1,
        unit_price=Money(100.0),
        total_price=Money(100.0)
    )
    booking.booking_id = "BKG001"
    booking.status = "Paid"

    # Add a checked-in ticket
    ticket = Ticket(ticket_code=TicketCode(), event_id="EV001")
    ticket.booking_id = "BKG001"
    ticket.status = TicketStatuses.CHECKED_IN
    booking.add_ticket(ticket)

    booking_repo.save(BookingAggregate(booking))

    handler = RequestRefundHandler(booking_repo, refund_repo)
    command = RequestRefundCommand(booking_id="BKG001")

    with pytest.raises(ValueError) as exc:
        handler.handle(command)
    assert "Refund cannot be requested if ticket has already been checked in" in str(exc.value)