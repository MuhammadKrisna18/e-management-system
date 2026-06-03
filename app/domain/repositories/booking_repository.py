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