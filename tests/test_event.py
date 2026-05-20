import pytest
from datetime import datetime

from app.domain.entities.event import Event
from app.domain.entities.ticket_category import TicketCategory
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.services.pricing_service import PricingService
from app.domain.value_objects.money import Money


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