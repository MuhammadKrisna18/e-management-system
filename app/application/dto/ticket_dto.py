from dataclasses import dataclass


@dataclass
class TicketDTO:

    code: str
    status: str

@dataclass
class PurchasedTicketDto:
    ticket_code: str
    event_id: str
    event_name: str
    ticket_category: str
    status: str

@dataclass
class PurchasedTicketsResponse:
    customer_id: str
    tickets: list[PurchasedTicketDto]