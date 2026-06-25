from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.entities.ticket import Ticket
from app.domain.value_objects.ticket_code import TicketCode
from app.infrastructure.database.models import TicketModel

class PostgresTicketRepository(TicketRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_code(self, ticket_code: str) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == ticket_code).first()
        if not model:
            return None
            
        ticket = Ticket(
            ticket_code=TicketCode(model.ticket_code),
            event_id=model.event_id
        )
        ticket.booking_id = model.booking_id
        ticket.status = model.status
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        # Since ticket_id might just mean the code in domain
        return self.find_by_code(ticket_id)

    def find_by_booking(self, booking_id: str) -> list:
        models = self.session.query(TicketModel).filter(TicketModel.booking_id == booking_id).all()
        return [self.find_by_code(model.ticket_code) for model in models if model]

    def find_by_event(self, event_id: str) -> list:
        models = self.session.query(TicketModel).filter(TicketModel.event_id == event_id).all()
        return [self.find_by_code(model.ticket_code) for model in models if model]

    def find_all(self) -> list:
        models = self.session.query(TicketModel).all()
        return [self.find_by_code(model.ticket_code) for model in models if model]

    def delete(self, ticket_id: str) -> bool:
        model = self.session.query(TicketModel).filter(TicketModel.ticket_code == ticket_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
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
