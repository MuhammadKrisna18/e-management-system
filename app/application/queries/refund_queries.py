

class GetRefundDetailsQuery:

    def __init__(self, refund_id: str):
        self.refund_id = refund_id


class GetCustomerRefundsQuery:

    def __init__(self, customer_id: str, page: int = 1, page_size: int = 10):
        self.customer_id = customer_id
        self.page = page
        self.page_size = page_size


class GetRefundByBookingQuery:

    def __init__(self, booking_id: str):
        self.booking_id = booking_id


class GetApprovedRefundsQuery:

    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size
