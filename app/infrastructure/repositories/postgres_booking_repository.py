from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.entities.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_code import TicketCode
from app.infrastructure.database.models import BookingModel, TicketModel

class PostgresBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, aggregate: BookingAggregate) -> None:
        booking = aggregate.booking
        
        model = self.session.query(BookingModel).filter(BookingModel.booking_id == booking.booking_id).first()
        if not model:
            model = BookingModel(booking_id=booking.booking_id)
            self.session.add(model)
            
        model.customer_id = booking.customer_id
        model.event_id = booking.event_id
        model.ticket_category_name = booking.ticket_category_name
        model.quantity = booking.quantity
        model.unit_price = booking.unit_price.amount
        model.total_price = booking.total_price.amount
        model.status = booking.status
        if booking.payment_deadline:
            model.payment_deadline = booking.payment_deadline.deadline
            
        # Sync tickets
        existing_tickets = {t.ticket_code: t for t in model.tickets}
        for ticket in booking.tickets:
            code_str = str(ticket.ticket_code.code)
            if code_str in existing_tickets:
                t_model = existing_tickets[code_str]
            else:
                t_model = TicketModel(booking_id=booking.booking_id, ticket_code=code_str)
                model.tickets.append(t_model)
                
            t_model.event_id = ticket.event_id
            t_model.status = ticket.status
            
        self.session.commit()

    def get_by_id(self, booking_id: str) -> Optional[BookingAggregate]:
        model = self.session.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()
        if not model:
            return None
            
        booking = Booking(
            customer_id=model.customer_id,
            event_id=model.event_id,
            ticket_category_name=model.ticket_category_name,
            quantity=model.quantity,
            unit_price=Money(model.unit_price),
            total_price=Money(model.total_price)
        )
        booking.booking_id = model.booking_id
        booking.status = model.status
        
        from app.domain.value_objects.payment_deadline import PaymentDeadline
        booking.payment_deadline = PaymentDeadline(model.payment_deadline)
        
        for t_model in model.tickets:
            t = Ticket(
                ticket_code=TicketCode(t_model.ticket_code),
                event_id=t_model.event_id
            )
            t.booking_id = t_model.booking_id
            t.status = t_model.status
            booking.tickets.append(t)
            
        return BookingAggregate(booking)
