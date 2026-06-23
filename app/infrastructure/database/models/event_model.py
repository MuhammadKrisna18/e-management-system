from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app.infrastructure.database.base import Base


class EventModel(Base):

    __tablename__ = "events"

    id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=False
    )