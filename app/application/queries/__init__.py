"""Application queries"""

from .get_available_events_query import GetAvailableEventsQuery
from .get_event_detail_query import GetEventDetailQuery
from .get_purchased_tickets_query import GetPurchasedTicketsQuery
from .get_sales_report_query import GetSalesReportQuery
from .get_participant_list_query import GetParticipantListQuery
from .get_booking_detail_query import GetBookingDetailQuery

__all__ = [
    "GetAvailableEventsQuery",
    "GetEventDetailQuery",
    "GetPurchasedTicketsQuery",
    "GetSalesReportQuery",
    "GetParticipantListQuery",
    "GetBookingDetailQuery",
]
