from math import ceil
from datetime import datetime
from app.application.queries.event_queries import (
    GetEventSalesReportQuery,
    GetEventParticipantsQuery,
)
from app.application.dto.event_report_dto import (
    CategorySalesDto,
    BookingStatsDto,
    EventSalesReportResponse,
    ParticipantDto,
    EventParticipantsResponse
)
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.ticket_repository import TicketRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.booking_status import BookingStatus


class GetEventSalesReportQueryHandler:

    def __init__(
        self,
        event_repository: EventRepository,
        booking_repository: BookingRepository,
        ticket_repository: TicketRepository,
    ):
        self.event_repository = event_repository
        self.booking_repository = booking_repository
        self.ticket_repository = ticket_repository

    def handle(self, query: GetEventSalesReportQuery) -> EventSalesReportResponse:
        event_agg = self.event_repository.get_by_id(query.event_id)
        if not event_agg:
            raise ValueError(f"Event {query.event_id} not found")

        category_sales = self._calculate_category_sales(event_agg, query.event_id)
        booking_stats, total_revenue = self._calculate_booking_stats(query.event_id)

        return EventSalesReportResponse(
            event_id=query.event_id,
            event_name=event_agg.event.name,
            category_sales=category_sales,
            booking_stats=booking_stats,
            total_revenue=total_revenue,
            report_generated_at=datetime.now().isoformat()
        )

    def _calculate_category_sales(self, event_agg, event_id: str) -> list:
        category_sales = []
        
        # Initialize all categories
        category_map = {}
        for category in event_agg.ticket_categories:
            category_map[category.name] = {
                "quota": category.quota,
                "sold": 0,
                "available": category.quota,
                "revenue": 0.0
            }

        # Count sold tickets and revenue
        for booking_agg in self.booking_repository.find_all():
            booking = booking_agg.booking
            if (booking.event_id == event_id 
                and booking.status == BookingStatus.PAID):
                category_name = getattr(booking, 'ticket_category_name', 'General')
                if category_name in category_map:
                    quantity = getattr(booking, 'quantity', 0)
                    category_map[category_name]["sold"] += quantity
                    category_map[category_name]["available"] -= quantity
                    # Add revenue if available
                    if hasattr(booking, 'total_price'):
                        category_map[category_name]["revenue"] += booking.total_price.amount

        # Convert to DTOs
        for name, data in category_map.items():
            category_sales.append(
                CategorySalesDto(
                    category_name=name,
                    quota=data["quota"],
                    sold=data["sold"],
                    available=data["available"],
                    revenue=data["revenue"]
                )
            )

        return category_sales

    def _calculate_booking_stats(self, event_id: str) -> tuple:
        pending_payment = 0
        paid = 0
        expired = 0
        refunded = 0
        total_revenue = 0.0

        for booking_agg in self.booking_repository.find_all():
            booking = booking_agg.booking
            if booking.event_id != event_id:
                continue

            if booking.status == BookingStatus.PENDING_PAYMENT:
                pending_payment += 1
            elif booking.status == BookingStatus.PAID:
                paid += 1
                if hasattr(booking, 'total_price'):
                    total_revenue += booking.total_price.amount
            elif booking.status == BookingStatus.EXPIRED:
                expired += 1
            elif booking.status == BookingStatus.REFUNDED:
                refunded += 1

        booking_stats = BookingStatsDto(
            pending_payment=pending_payment,
            paid=paid,
            expired=expired,
            refunded=refunded
        )
        
        return booking_stats, total_revenue


class GetEventParticipantsQueryHandler:

    def __init__(
        self,
        event_repository: EventRepository,
        booking_repository: BookingRepository,
        ticket_repository: TicketRepository,
    ):
        self.event_repository = event_repository
        self.booking_repository = booking_repository
        self.ticket_repository = ticket_repository

    def handle(self, query: GetEventParticipantsQuery) -> EventParticipantsResponse:
        event_agg = self.event_repository.get_by_id(query.event_id)
        if not event_agg:
            raise ValueError(f"Event {query.event_id} not found")

        participants = self._collect_participants(query.event_id)
        paginated = self._paginate_results(participants, query.page, query.page_size)
        
        total_pages = (len(participants) + query.page_size - 1) // query.page_size

        return EventParticipantsResponse(
            event_id=query.event_id,
            event_name=event_agg.event.name,
            participants=paginated,
            total=len(participants),
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
            generated_at=datetime.now().isoformat()
        )

    def _collect_participants(self, event_id: str) -> list:
        participants = []

        for booking_agg in self.booking_repository.find_all():
            booking = booking_agg.booking
            if (booking.event_id != event_id 
                or booking.status != BookingStatus.PAID):
                continue

            # Get tickets for this booking
            tickets = self.ticket_repository.find_by_booking(booking.booking_id)
            for ticket in tickets:
                ticket_code = getattr(ticket, 'ticket_code', None)
                if hasattr(ticket_code, 'code'):
                    code = ticket_code.code
                else:
                    code = getattr(ticket, 'code', 'N/A')
                
                checked_in_at = None
                status = getattr(ticket, 'status', 'Active')
                if hasattr(ticket, 'checked_in_at'):
                    checked_in_at = ticket.checked_in_at.isoformat() if ticket.checked_in_at else None

                participants.append(
                    ParticipantDto(
                        customer_id=booking.customer_id,
                        ticket_category=getattr(booking, 'ticket_category_name', 'General'),
                        ticket_code=code,
                        check_in_status=str(status),
                        checked_in_at=checked_in_at
                    )
                )

        return participants

    def _paginate_results(self, items: list, page: int, page_size: int) -> list:
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return items[start_idx:end_idx]
