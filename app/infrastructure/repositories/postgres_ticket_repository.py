from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.infrastructure.database.models import TicketModel


class PostgresTicketRepository(TicketRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, ticket: Ticket) -> str:
        code_str = str(ticket.ticket_code.value)
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == code_str).first()
        if not model:
            model = TicketModel(ticket_code=code_str)
            self.session.add(model)

        model.booking_id = ticket.booking_id
        model.event_id = ticket.event_id
        model.status = ticket.status.value if hasattr(ticket.status, 'value') else str(ticket.status)
        self.session.commit()
        return code_str

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self.find_by_code(ticket_id)

    def find_by_code(self, ticket_code: str) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == ticket_code).first()
        if not model:
            return None
        return self._to_domain(model)

    def find_by_booking(self, booking_id: str) -> List[Ticket]:
        models = self.session.query(TicketModel).filter(TicketModel.booking_id == booking_id).all()
        return [self._to_domain(m) for m in models]

    def find_by_event(self, event_id: str) -> List[Ticket]:
        models = self.session.query(TicketModel).filter(TicketModel.event_id == event_id).all()
        return [self._to_domain(m) for m in models]

    def find_all(self) -> List[Ticket]:
        models = self.session.query(TicketModel).all()
        return [self._to_domain(m) for m in models]

    def delete(self, ticket_id: str) -> bool:
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == ticket_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False

    def _to_domain(self, model: TicketModel) -> Ticket:
        from app.domain.value_objects.ticket_status import TicketStatus
        ticket = Ticket(
            ticket_code=TicketCode(model.ticket_code),
            event_id=model.event_id
        )
        ticket.booking_id = model.booking_id
        ticket.status = TicketStatus(model.status) if model.status else ticket.status
        return ticket
