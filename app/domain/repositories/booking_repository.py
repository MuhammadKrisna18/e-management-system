from abc import ABC
from abc import abstractmethod


class BookingRepository(
    ABC
):

    @abstractmethod
    def save(
        self,
        booking
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        booking_id
    ):
        pass

    @abstractmethod
    def find_active_by_customer_and_event(
        self,
        customer_id: str,
        event_id: str
    ):
        pass

    @abstractmethod
    def get_booked_quantity_for_category(
        self,
        event_id: str,
        ticket_category_name: str
    ) -> int:
        pass