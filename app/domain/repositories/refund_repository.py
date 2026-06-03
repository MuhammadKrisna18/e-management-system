from abc import ABC
from abc import abstractmethod


class RefundRepository(
    ABC
):

    @abstractmethod
    def save(
        self,
        refund
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        refund_id
    ):
        pass