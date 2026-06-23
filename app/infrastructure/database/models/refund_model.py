from sqlalchemy import Column
from sqlalchemy import String

from app.infrastructure.database.base import Base


class RefundModel(Base):

    __tablename__ = "refunds"

    id = Column(
        String,
        primary_key=True
    )

    status = Column(
        String,
        nullable=False
    )