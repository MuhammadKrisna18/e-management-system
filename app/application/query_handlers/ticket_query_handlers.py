from typing import List
from app.application.queries.ticket_queries import GetPurchasedTicketsQuery
from app.application.dto.ticket_dto import PurchasedTicketDto, PurchasedTicketsResponse
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.constants import BookingStatuses, EventStatus, TicketStatuses

class GetPurchasedTicketsQueryHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        ticket_repository: TicketRepository,
        event_repository: EventRepository
    ):
        self.booking_repository = booking_repository
        self.ticket_repository = ticket_repository
        self.event_repository = event_repository

    def handle(self, query: GetPurchasedTicketsQuery) -> PurchasedTicketsResponse:
        purchased_tickets = []
        
        # 1. Find all paid bookings for the customer
        for booking_agg in self.booking_repository.find_all():
            booking = booking_agg.booking
            if booking.customer_id != query.customer_id:
                continue
                
            # AC: Customers can only view tickets from bookings with the status Paid.
            if booking.status != BookingStatuses.PAID:
                continue
                
            # Fetch the event to get the name and status
            event_agg = self.event_repository.get_by_id(booking.event_id)
            if not event_agg:
                continue
            event_name = event_agg.event.name
            is_event_cancelled = event_agg.event.status == EventStatus.CANCELLED
            
            # 2. Get tickets for this booking
            tickets = self.ticket_repository.find_by_booking(booking.booking_id)
            
            for ticket in tickets:
                ticket_code_val = getattr(ticket.ticket_code, 'value', ticket.ticket_code)
                
                # Ticket status logic
                status = ticket.status
                
                # AC: Tickets from cancelled events must have the status Cancelled or RefundRequired.
                if is_event_cancelled:
                    if status != TicketStatuses.CANCELLED:
                        status = "RefundRequired"
                
                purchased_tickets.append(
                    PurchasedTicketDto(
                        ticket_code=ticket_code_val,
                        event_id=booking.event_id,
                        event_name=event_name,
                        ticket_category=booking.ticket_category_name,
                        status=status
                    )
                )

        return PurchasedTicketsResponse(
            customer_id=query.customer_id,
            tickets=purchased_tickets
        )
