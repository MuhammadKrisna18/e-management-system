from sqlalchemy import Column
from sqlalchemy import String

from app.infrastructure.database.base import Base


class TicketModel(Base):

    __tablename__ = "tickets"

    id = Column(
        String,
        primary_key=True
    )

    ticket_code = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )