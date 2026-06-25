from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class AvailableEventDto:
    event_id: str
    name: str
    start_date: datetime
    location: str
    lowest_ticket_price: float

@dataclass
class AvailableEventsResponse:
    events: List[AvailableEventDto]

@dataclass
class TicketCategoryDetailDto:
    name: str
    price: float
    status: str

@dataclass
class EventDetailResponse:
    event_id: str
    name: str
    description: str
    start_date: datetime
    location: str
    organizer: str
    ticket_categories: List[TicketCategoryDetailDto]

@dataclass
class EventDTO:
    id: str
    name: str
    status: str