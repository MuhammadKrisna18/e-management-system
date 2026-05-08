"""Cancel Event Command"""


class CancelEventCommand:
    """Command to cancel an event"""

    def __init__(self, event_id: str, reason: str):
        self.event_id = event_id
        self.reason = reason
