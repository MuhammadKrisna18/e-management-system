from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.aggregates.booking_aggregate import BookingAggregate
from app.domain.entities.booking import Booking
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.money import Money
from app.domain.value_objects.ticket_code import TicketCode
from app.domain.value_objects.payment_deadline import PaymentDeadline
from app.domain.value_objects.booking_status import BookingStatus
from app.infrastructure.database.models import BookingModel, TicketModel


class PostgresBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, aggregate: BookingAggregate) -> str:
        booking = aggregate.booking
        model = self.session.query(BookingModel).filter(BookingModel.booking_id == booking.booking_id).first()
        if not model:
            model = BookingModel(booking_id=booking.booking_id)
            self.session.add(model)

        model.customer_id = booking.customer_id
        model.event_id = booking.event_id
        model.ticket_category_name = booking.ticket_category_name
        model.quantity = booking.quantity
        model.unit_price = booking.unit_price.amount if hasattr(booking.unit_price, 'amount') else float(booking.unit_price)
        model.total_price = booking.total_price.amount if hasattr(booking.total_price, 'amount') else float(booking.total_price)
        model.status = booking.status.value if hasattr(booking.status, 'value') else str(booking.status)
        model.payment_deadline = booking.payment_deadline.deadline

        # Sync tickets
        existing_tickets = {t.ticket_code: t for t in model.tickets}
        for ticket in booking.tickets:
            code_str = str(ticket.ticket_code.value)
            if code_str in existing_tickets:
                t_model = existing_tickets[code_str]
            else:
                t_model = TicketModel(booking_id=booking.booking_id, ticket_code=code_str)
                model.tickets.append(t_model)
            t_model.event_id = ticket.event_id
            t_model.status = ticket.status.value if hasattr(ticket.status, 'value') else str(ticket.status)

        self.session.commit()
        return booking.booking_id

    def get_by_id(self, booking_id: str) -> Optional[BookingAggregate]:
        model = self.session.query(BookingModel).filter(BookingModel.booking_id == booking_id).first()
        if not model:
            return None
        return self._to_aggregate(model)

    def find_active_by_customer_and_event(self, customer_id: str, event_id: str) -> List[BookingAggregate]:
        models = self.session.query(BookingModel).filter(
            BookingModel.customer_id == customer_id,
            BookingModel.event_id == event_id,
            BookingModel.status.in_([BookingStatus.PENDING_PAYMENT.value, BookingStatus.PAID.value])
        ).all()
        return [self._to_aggregate(m) for m in models]

    def get_booked_quantity_for_category(self, event_id: str, ticket_category_name: str) -> int:
        from sqlalchemy import func
        result = self.session.query(func.sum(BookingModel.quantity)).filter(
            BookingModel.event_id == event_id,
            BookingModel.ticket_category_name == ticket_category_name,
            BookingModel.status.in_([BookingStatus.PENDING_PAYMENT.value, BookingStatus.PAID.value])
        ).scalar()
        return result or 0

    def find_all(self) -> List[BookingAggregate]:
        models = self.session.query(BookingModel).all()
        return [self._to_aggregate(m) for m in models]

    def _to_aggregate(self, model: BookingModel) -> BookingAggregate:
        from app.domain.value_objects.ticket_status import TicketStatus
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
        booking.payment_deadline = PaymentDeadline(model.payment_deadline)

        for t_model in model.tickets:
            t = Ticket(
                ticket_code=TicketCode(t_model.ticket_code),
                event_id=t_model.event_id
            )
            t.booking_id = t_model.booking_id
            t.status = TicketStatus(t_model.status) if t_model.status else t.status
            booking.tickets.append(t)

        return BookingAggregate(booking)

    def find_active_by_customer_and_event(
        self,
        customer_id: str,
        event_id: str
    ) -> Optional[BookingAggregate]:
        model = self.session.query(BookingModel).filter(
            BookingModel.customer_id == customer_id,
            BookingModel.event_id == event_id,
            BookingModel.status.in_(["Pending", "Paid"])
        ).first()
        if not model:
            return None
        return self.get_by_id(model.booking_id)

    def get_booked_quantity_for_category(
        self,
        event_id: str,
        ticket_category_name: str
    ) -> int:
        from sqlalchemy import func
        result = self.session.query(func.sum(BookingModel.quantity)).filter(
            BookingModel.event_id == event_id,
            BookingModel.ticket_category_name == ticket_category_name,
            BookingModel.status.in_(["Pending", "Paid"])
        ).scalar()
        return result or 0
