from abc import ABC, abstractmethod


class EventRepository(ABC):

    @abstractmethod
    def save(self, event):
        pass

    @abstractmethod
    def get_by_id(self, event_id):
        pass