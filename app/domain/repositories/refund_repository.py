from abc import ABC
from abc import abstractmethod
from typing import List, Optional


class RefundRepository(ABC):

    @abstractmethod
    def save(self, refund_aggregate) -> str:
        pass

    @abstractmethod
    def get_by_id(self, refund_id: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_booking(self, booking_id: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[object]:
        pass

    @abstractmethod
    def find_approved_pending_payout(self) -> List[object]:
        pass

    @abstractmethod
    def find_all(self) -> List[object]:
        pass

    @abstractmethod
    def delete(self, refund_id: str) -> bool:
        pass