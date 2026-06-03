from abc import ABC
from abc import abstractmethod


class NotificationService(
    ABC
):

    @abstractmethod
    def send(
        self,
        destination,
        message
    ):
        pass