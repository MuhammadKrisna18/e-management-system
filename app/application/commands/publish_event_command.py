"""Publish Event Command"""


class PublishEventCommand:
    """Command to publish an event"""

    def __init__(self, event_id: str):
        self.event_id = event_id
