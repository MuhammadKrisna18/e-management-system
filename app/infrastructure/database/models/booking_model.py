from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from app.infrastructure.database.base import Base


class BookingModel(Base):

    __tablename__ = "bookings"

    id = Column(
        String,
        primary_key=True
    )

    status = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )