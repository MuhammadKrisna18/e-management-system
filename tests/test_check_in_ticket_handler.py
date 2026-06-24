import pytest
from datetime import datetime, timedelta
from app.application.commands.check_in_ticket_command import CheckInTicketCommand
from app.application.command_handlers.check_in_ticket_handler import CheckInTicketHandler
from app.domain.entities.ticket import Ticket
from app.domain.entities.event import Event
from app.domain.aggregates.event_aggregate import EventAggregate
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.constants import EventStatus, TicketStatuses as TicketStatus
from app.infrastructure.repositories.in_memory_ticket_repository import InMemoryTicketRepository
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository

def test_check_in_ticket_success():
    # Setup
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    
    # Event currently active
    event = Event("Tech", datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1), 100)
    event.event_id = "EV001"
    event.status = EventStatus.PUBLISHED
    event_repo.save(EventAggregate(event))
    
    ticket = Ticket(TicketCode(), "EV001")
    ticket.ticket_id = "TKT1"
    ticket_code_val = ticket.ticket_code.value
    ticket_repo.save(ticket)
    
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand(ticket_code_val, "EV001")
    
    # Execute
    res = handler.handle(command)
    
    # Verify
    assert res == ticket_code_val
    updated_ticket = ticket_repo.get_by_id("TKT1")
    assert updated_ticket.status == TicketStatus.CHECKED_IN

def test_check_in_invalid_ticket():
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand("INVALID", "EV001")
    
    with pytest.raises(ValueError, match="Ticket is invalid"):
        handler.handle(command)

def test_check_in_already_used():
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    
    event = Event("Tech", datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1), 100)
    event.event_id = "EV001"
    event_repo.save(EventAggregate(event))
    
    ticket = Ticket(TicketCode(), "EV001")
    ticket.check_in()
    ticket_repo.save(ticket)
    
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand(ticket.ticket_code.value, "EV001")
    
    with pytest.raises(ValueError, match="Ticket has already been used"):
        handler.handle(command)

def test_check_in_wrong_event():
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    
    ticket = Ticket(TicketCode(), "EV002") # Belongs to EV002
    ticket_repo.save(ticket)
    
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand(ticket.ticket_code.value, "EV001")
    
    with pytest.raises(ValueError, match="Ticket does not match the event"):
        handler.handle(command)

def test_check_in_cancelled_event():
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    
    event = Event("Tech", datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1), 100)
    event.event_id = "EV001"
    event.status = EventStatus.CANCELLED
    event_repo.save(EventAggregate(event))
    
    ticket = Ticket(TicketCode(), "EV001")
    ticket_repo.save(ticket)
    
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand(ticket.ticket_code.value, "EV001")
    
    with pytest.raises(ValueError, match="Event has been cancelled"):
        handler.handle(command)

def test_check_in_outside_window():
    ticket_repo = InMemoryTicketRepository()
    event_repo = InMemoryEventRepository()
    
    # Event ended yesterday
    event = Event("Tech", datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1), 100)
    event.event_id = "EV001"
    event_repo.save(EventAggregate(event))
    
    ticket = Ticket(TicketCode(), "EV001")
    ticket_repo.save(ticket)
    
    handler = CheckInTicketHandler(ticket_repo, event_repo)
    command = CheckInTicketCommand(ticket.ticket_code.value, "EV001")
    
    with pytest.raises(ValueError, match="Check-in outside allowed time window"):
        handler.handle(command)
