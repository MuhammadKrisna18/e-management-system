from abc import ABC
from abc import abstractmethod
from typing import List, Optional


class TicketRepository(ABC):

    @abstractmethod
    def save(self, ticket) -> str:
        pass

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_booking(self, booking_id: str) -> List[object]:
        pass

    @abstractmethod
    def find_by_code(self, ticket_code: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_event(self, event_id: str) -> List[object]:
        pass

    @abstractmethod
    def find_all(self) -> List[object]:
        pass

    @abstractmethod
    def delete(self, ticket_id: str) -> bool:
        pass
