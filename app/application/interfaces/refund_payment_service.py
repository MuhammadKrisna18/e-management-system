from abc import ABC
from abc import abstractmethod


class RefundPaymentService(
    ABC
):

    @abstractmethod
    def transfer(
        self,
        amount
    ):
        pass