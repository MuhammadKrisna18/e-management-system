from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.infrastructure.database.models import TicketModel

class PostgresTicketRepository(TicketRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: str) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == code).first()
        if not model:
            return None
            
        ticket = Ticket(
            ticket_code=TicketCode(model.ticket_code),
            event_id=model.event_id
        )
        ticket.booking_id = model.booking_id
        ticket.status = model.status
        return ticket

    def save(self, ticket: Ticket) -> None:
        code_str = str(ticket.ticket_code.code)
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == code_str).first()
        if not model:
            model = TicketModel(ticket_code=code_str)
            self.session.add(model)
            
        model.booking_id = ticket.booking_id
        model.event_id = ticket.event_id
        model.status = ticket.status
        self.session.commit()
