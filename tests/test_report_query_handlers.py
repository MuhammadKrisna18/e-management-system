import pytest
from datetime import datetime, timedelta

from app.application.queries.event_queries import GetEventSalesReportQuery, GetEventParticipantsQuery
from app.application.query_handlers.report_query_handlers import GetEventSalesReportQueryHandler, GetEventParticipantsQueryHandler

from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_booking_repository import InMemoryBookingRepository
from app.infrastructure.repositories.in_memory_ticket_repository import InMemoryTicketRepository

from app.domain.entities.event import Event
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.entities.ticket_category import TicketCategory

from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.value_objects.money import Money
from app.domain.constants import BookingStatuses, TicketStatuses

def setup_test_data():
    event_repo = InMemoryEventRepository()
    booking_repo = InMemoryBookingRepository()
    ticket_repo = InMemoryTicketRepository()
    
    # 1. Create Event
    event = Event("Test Event", datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=1), 100)
    event.event_id = "EV001"
    event_agg = EventAggregate(event)
    now = datetime.now()
    event_agg.add_ticket_category(TicketCategory("VIP", 100.0, 20, now, now + timedelta(days=1), now + timedelta(days=2)))
    event_agg.add_ticket_category(TicketCategory("Regular", 50.0, 80, now, now + timedelta(days=1), now + timedelta(days=2)))
    event_repo.save(event_agg)
    
    # 2. Create Bookings
    # Booking 1: PAID (VIP, 2 tickets)
    b1 = Booking("C1", "EV001", "VIP", 2, Money(100.0), Money(200.0))
    b1.booking_id = "BK1"
    b1.status = BookingStatuses.PAID
    b1_agg = BookingAggregate(b1)
    booking_repo.save(b1_agg)
    
    # Create tickets for BK1
    from app.domain.entities.ticket import Ticket
    from app.domain.value_objects.ticket_code import TicketCode
    
    t1 = Ticket(TicketCode(), "EV001")
    t1.booking_id = "BK1"
    t1.status = TicketStatuses.ACTIVE
    ticket_repo.save(t1)
    b1.add_ticket(t1)
    
    t2 = Ticket(TicketCode(), "EV001")
    t2.booking_id = "BK1"
    t2.status = TicketStatuses.CHECKED_IN
    ticket_repo.save(t2)
    b1.add_ticket(t2)

    # Booking 2: PENDING (Regular, 3 tickets)
    b2 = Booking("C2", "EV001", "Regular", 3, Money(50.0), Money(150.0))
    b2.booking_id = "BK2"
    b2.status = BookingStatuses.PENDING_PAYMENT
    b2_agg = BookingAggregate(b2)
    booking_repo.save(b2_agg)

    # Booking 3: EXPIRED (VIP, 1 ticket)
    b3 = Booking("C3", "EV001", "VIP", 1, Money(100.0), Money(100.0))
    b3.booking_id = "BK3"
    b3.status = BookingStatuses.EXPIRED
    b3_agg = BookingAggregate(b3)
    booking_repo.save(b3_agg)

    # Booking 4: REFUNDED (Regular, 2 tickets)
    b4 = Booking("C4", "EV001", "Regular", 2, Money(50.0), Money(100.0))
    b4.booking_id = "BK4"
    b4.status = BookingStatuses.REFUNDED
    b4_agg = BookingAggregate(b4)
    booking_repo.save(b4_agg)
    
    return event_repo, booking_repo, ticket_repo

def test_get_event_sales_report():
    event_repo, booking_repo, ticket_repo = setup_test_data()
    
    handler = GetEventSalesReportQueryHandler(event_repo, booking_repo, ticket_repo)
    query = GetEventSalesReportQuery("EV001")
    
    response = handler.handle(query)
    
    assert response.event_id == "EV001"
    assert response.total_revenue == 200.0 # Only paid bookings (BK1)
    assert response.booking_stats.paid == 1
    assert response.booking_stats.pending_payment == 1
    assert response.booking_stats.expired == 1
    assert response.booking_stats.refunded == 1
    
    # Check category sales
    vip_sales = next(c for c in response.category_sales if c.category_name == "VIP")
    assert vip_sales.sold == 2
    assert vip_sales.revenue == 200.0
    
    reg_sales = next(c for c in response.category_sales if c.category_name == "Regular")
    assert reg_sales.sold == 0  # no paid regular bookings
    assert reg_sales.revenue == 0.0

def test_get_event_participants():
    event_repo, booking_repo, ticket_repo = setup_test_data()
    
    handler = GetEventParticipantsQueryHandler(event_repo, booking_repo, ticket_repo)
    query = GetEventParticipantsQuery("EV001", page=1, page_size=10)
    
    response = handler.handle(query)
    
    assert response.event_id == "EV001"
    assert response.total == 2 # BK1 has 2 tickets (paid)
    assert len(response.participants) == 2
    
    # One ticket active, one checked in
    statuses = [p.check_in_status for p in response.participants]
    assert TicketStatuses.ACTIVE in statuses
    assert TicketStatuses.CHECKED_IN in statuses
