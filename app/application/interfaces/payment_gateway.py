from abc import ABC
from abc import abstractmethod


class PaymentGateway(
    ABC
):

    @abstractmethod
    def charge(
        self,
        amount
    ):
        pass