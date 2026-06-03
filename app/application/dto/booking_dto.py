from dataclasses import dataclass


@dataclass
class BookingDTO:

    id: str
    status: str
    total_price: float