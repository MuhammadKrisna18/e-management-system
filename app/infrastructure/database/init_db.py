from app.infrastructure.database.base import Base
from app.infrastructure.database.connection import engine

from app.infrastructure.database.models.event_model import EventModel
from app.infrastructure.database.models.booking_model import BookingModel
from app.infrastructure.database.models.refund_model import RefundModel
from app.infrastructure.database.models.ticket_model import TicketModel
from app.infrastructure.database.models.ticket_category_model import (
    TicketCategoryModel
)

Base.metadata.create_all(
    bind=engine
)

print(
    "Database tables created successfully."
)