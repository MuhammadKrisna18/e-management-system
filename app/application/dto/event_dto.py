from dataclasses import dataclass


@dataclass
class EventDTO:

    id: str
    name: str
    status: str