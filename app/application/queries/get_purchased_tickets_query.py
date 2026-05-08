"""Get Purchased Tickets Query"""

from typing import Optional


class GetPurchasedTicketsQuery:
    """Query to get purchased tickets"""

    def __init__(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
    ):
        self.user_id = user_id
        self.skip = skip
        self.limit = limit
        self.status = status
