"""Refund Query Definitions"""


class GetRefundDetailsQuery:
    """
    Query to get details of a specific refund.
    
    Used for User Story 15: View Refund Details
    """

    def __init__(self, refund_id: str):
        """
        Initialize GetRefundDetailsQuery.
        
        Args:
            refund_id: ID of the refund to retrieve
        """
        self.refund_id = refund_id


class GetCustomerRefundsQuery:
    """
    Query to get all refunds for a customer.
    
    Used for User Story 15: View Refund Details
    """

    def __init__(self, customer_id: str, page: int = 1, page_size: int = 10):
        """
        Initialize GetCustomerRefundsQuery.
        
        Args:
            customer_id: ID of the customer
            page: Page number for pagination
            page_size: Number of items per page
        """
        self.customer_id = customer_id
        self.page = page
        self.page_size = page_size


class GetRefundByBookingQuery:
    """
    Query to get refund for a booking.
    
    Used internally to find refund by booking ID
    """

    def __init__(self, booking_id: str):
        """
        Initialize GetRefundByBookingQuery.
        
        Args:
            booking_id: ID of the booking
        """
        self.booking_id = booking_id


class GetApprovedRefundsQuery:
    """
    Query to get approved refunds pending payout.
    
    Used for User Story 18: Mark Refund as Paid Out
    """

    def __init__(self, page: int = 1, page_size: int = 10):
        """
        Initialize GetApprovedRefundsQuery.
        
        Args:
            page: Page number for pagination
            page_size: Number of items per page
        """
        self.page = page
        self.page_size = page_size
