import pytest
from datetime import datetime, timedelta

from app.application.queries.ticket_queries import GetPurchasedTicketsQuery
from app.application.query_handlers.ticket_query_handlers import GetPurchasedTicketsQueryHandler

from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_booking_repository import InMemoryBookingRepository
from app.infrastructure.repositories.in_memory_ticket_repository import InMemoryTicketRepository

from app.domain.entities.event import Event
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.entities.ticket_category import TicketCategory

from app.domain.entities.booking import Booking
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.value_objects.money import Money
from app.domain.constants import BookingStatuses, EventStatus, TicketStatuses

from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode

def setup_test_data():
    event_repo = InMemoryEventRepository()
    booking_repo = InMemoryBookingRepository()
    ticket_repo = InMemoryTicketRepository()
    
    now = datetime.now()
    
    # 1. Create Event 1 (Active)
    event1 = Event("Tech Conf", now - timedelta(days=1), now + timedelta(days=1), 100)
    event1.event_id = "EV001"
    event1.status = EventStatus.PUBLISHED
    event1_agg = EventAggregate(event1)
    event1_agg.add_ticket_category(TicketCategory("VIP", 100.0, 20, now, now + timedelta(days=1), now + timedelta(days=2)))
    event_repo.save(event1_agg)
    
    # 2. Create Event 2 (Cancelled)
    event2 = Event("Music Fest", now - timedelta(days=1), now + timedelta(days=1), 100)
    event2.event_id = "EV002"
    event2.status = EventStatus.CANCELLED
    event2_agg = EventAggregate(event2)
    event2_agg.add_ticket_category(TicketCategory("Regular", 50.0, 20, now, now + timedelta(days=1), now + timedelta(days=2)))
    event_repo.save(event2_agg)

    customer_id = "CUST123"

    # Booking 1: PAID, EV001 (Should appear)
    b1 = Booking(customer_id, "EV001", "VIP", 2, Money(100.0), Money(200.0))
    b1.booking_id = "BK1"
    b1.status = BookingStatuses.PAID
    b1_agg = BookingAggregate(b1)
    booking_repo.save(b1_agg)
    
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

    # Booking 2: PENDING, EV001 (Should NOT appear)
    b2 = Booking(customer_id, "EV001", "VIP", 1, Money(100.0), Money(100.0))
    b2.booking_id = "BK2"
    b2.status = BookingStatuses.PENDING_PAYMENT
    b2_agg = BookingAggregate(b2)
    booking_repo.save(b2_agg)
    
    t3 = Ticket(TicketCode(), "EV001")
    t3.booking_id = "BK2"
    t3.status = TicketStatuses.ACTIVE
    ticket_repo.save(t3)
    b2.add_ticket(t3)

    # Booking 3: PAID, EV002 (Cancelled event - should appear but with Cancelled/RefundRequired status)
    b3 = Booking(customer_id, "EV002", "Regular", 1, Money(50.0), Money(50.0))
    b3.booking_id = "BK3"
    b3.status = BookingStatuses.PAID
    b3_agg = BookingAggregate(b3)
    booking_repo.save(b3_agg)
    
    t4 = Ticket(TicketCode(), "EV002")
    t4.booking_id = "BK3"
    t4.status = TicketStatuses.ACTIVE
    ticket_repo.save(t4)
    b3.add_ticket(t4)
    
    return event_repo, booking_repo, ticket_repo

def test_get_purchased_tickets():
    event_repo, booking_repo, ticket_repo = setup_test_data()
    
    handler = GetPurchasedTicketsQueryHandler(booking_repo, ticket_repo, event_repo)
    query = GetPurchasedTicketsQuery("CUST123")
    
    response = handler.handle(query)
    
    assert response.customer_id == "CUST123"
    assert len(response.tickets) == 3
    
    # 2 tickets from BK1 (EV001), 1 ticket from BK3 (EV002)
    ev1_tickets = [t for t in response.tickets if t.event_id == "EV001"]
    assert len(ev1_tickets) == 2
    assert ev1_tickets[0].event_name == "Tech Conf"
    assert ev1_tickets[0].ticket_category == "VIP"
    
    # Check statuses
    statuses = [t.status for t in ev1_tickets]
    assert TicketStatuses.ACTIVE in statuses
    assert TicketStatuses.CHECKED_IN in statuses
    
    # Ticket from cancelled event (EV002)
    ev2_tickets = [t for t in response.tickets if t.event_id == "EV002"]
    assert len(ev2_tickets) == 1
    assert ev2_tickets[0].event_name == "Music Fest"
    assert ev2_tickets[0].status == "RefundRequired"
