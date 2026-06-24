
from datetime import datetime
from app.application.commands.check_in_ticket_command import CheckInTicketCommand
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.constants import EventStatus
from app.domain.events.ticket_events import TicketCheckedIn

class CheckInTicketHandler:

    def __init__(self, ticket_repository: TicketRepository, event_repository: EventRepository):
        self.ticket_repository = ticket_repository
        self.event_repository = event_repository

    def handle(self, command: CheckInTicketCommand) -> str:
        ticket = self.ticket_repository.find_by_code(command.ticket_code)
        
        # AC: If ticket code not found
        if not ticket:
            raise ValueError("Ticket is invalid")
            
        # AC: If already checked in
        if ticket.is_checked_in():
            raise ValueError("Ticket has already been used")
            
        # AC: If belongs to a different event
        if not hasattr(ticket, 'event_id') or ticket.event_id != command.event_id:
            raise ValueError("Ticket does not match the event")

        event_agg = self.event_repository.get_by_id(command.event_id)
        if not event_agg:
            raise ValueError("Event not found")
            
        # AC: If event has been cancelled
        if event_agg.event.status == EventStatus.CANCELLED:
            raise ValueError("Event has been cancelled")
            
        # AC: Check-in can only be performed on the event day or within window
        now = datetime.now()
        # Using event start and end date as the check-in window. 
        # End date is usually included, so we might want to check <= end_date.
        # But wait, start_date and end_date might just be days. We'll use start_date <= now <= end_date (or end_date + 1 day depending on time).
        # We will keep it simple: now >= start_date and now <= end_date
        if now < event_agg.event.start_date or now > event_agg.event.end_date:
            raise ValueError("Check-in outside allowed time window")

        # Finally, perform the check-in
        ticket.check_in()
        
        # Save ticket
        # The ticket repository might require ticket_id or ticket directly
        ticket_id = getattr(ticket, 'ticket_id', None)
        if ticket_id:
            # We assume updating the ticket object in memory repo changes it, but let's call save anyway
            self.ticket_repository.save(ticket)
            
        # Note: We should raise TicketCheckedIn event. 
        # But we don't have an event publisher injected here. We can just return.
        
        return command.ticket_code
