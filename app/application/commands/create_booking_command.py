"""Create Booking Command"""

from typing import List


class CreateBookingCommand:
    """Command to create a new booking"""

    def __init__(
        self,
        user_id: str,
        event_id: str,
        ticket_items: List[dict],
        attendee_name: str,
        attendee_email: str,
    ):
        self.user_id = user_id
        self.event_id = event_id
        self.ticket_items = ticket_items  # [{ticket_category_id, quantity}, ...]
        self.attendee_name = attendee_name
        self.attendee_email = attendee_email
