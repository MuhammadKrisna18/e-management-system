from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from app.infrastructure.database.base import Base


class TicketCategoryModel(Base):

    __tablename__ = "ticket_categories"

    id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    quota = Column(
        Integer,
        nullable=False
    )