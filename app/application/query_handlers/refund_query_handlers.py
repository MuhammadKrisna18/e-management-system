"""Query Handlers for Refund Queries"""
from math import ceil
from app.application.queries.refund_queries import (
    GetRefundDetailsQuery,
    GetCustomerRefundsQuery,
    GetRefundByBookingQuery,
    GetApprovedRefundsQuery
)
from app.application.dto.refund_dto import (
    RefundDetailResponse,
    RefundSummaryResponse,
    RefundListResponse
)
from app.domain.repositories.refund_repository import RefundRepository


class GetRefundDetailsQueryHandler:
    """
    Handler for GetRefundDetailsQuery.
    Retrieves detailed information about a specific refund (US15).
    """

    def __init__(self, refund_repository: RefundRepository):
        """
        Initialize handler with refund repository.
        
        Args:
            refund_repository: RefundRepository instance
        """
        self.refund_repository = refund_repository

    def handle(self, query: GetRefundDetailsQuery) -> RefundDetailResponse:
        """
        Handle GetRefundDetailsQuery.
        
        Args:
            query: GetRefundDetailsQuery with refund_id
            
        Returns:
            RefundDetailResponse: Refund details
            
        Raises:
            ValueError: If refund not found
        """
        refund_agg = self.refund_repository.get_by_id(query.refund_id)
        if not refund_agg:
            raise ValueError(f"Refund {query.refund_id} not found")

        refund = refund_agg.refund

        return RefundDetailResponse(
            refund_id=refund.refund_id,
            booking_id=refund.booking_id,
            customer_id=refund.customer_id,
            event_id=refund.event_id,
            refund_amount=refund.refund_amount.amount,
            status=str(refund.status),
            created_at=refund.created_at.isoformat(),
            refund_deadline=refund.refund_deadline.isoformat(),
            rejection_reason=refund.rejection_reason,
            payment_reference=refund.payment_reference,
            approved_at=refund.approved_at.isoformat() if refund.approved_at else None,
            rejected_at=refund.rejected_at.isoformat() if refund.rejected_at else None,
            paid_out_at=refund.paid_out_at.isoformat() if refund.paid_out_at else None,
        )


class GetCustomerRefundsQueryHandler:
    """
    Handler for GetCustomerRefundsQuery.
    Retrieves all refunds for a customer with pagination (US15).
    """

    def __init__(self, refund_repository: RefundRepository):
        """
        Initialize handler with refund repository.
        
        Args:
            refund_repository: RefundRepository instance
        """
        self.refund_repository = refund_repository

    def handle(self, query: GetCustomerRefundsQuery) -> RefundListResponse:
        """
        Handle GetCustomerRefundsQuery.
        
        Args:
            query: GetCustomerRefundsQuery with customer_id
            
        Returns:
            RefundListResponse: Paginated list of refunds
        """
        # Get all refunds for customer
        refund_aggs = self.refund_repository.find_by_customer(query.customer_id)

        # Convert to summary DTOs
        summaries = [
            RefundSummaryResponse(
                refund_id=agg.refund.refund_id,
                booking_id=agg.refund.booking_id,
                refund_amount=agg.refund.refund_amount.amount,
                status=str(agg.refund.status),
                created_at=agg.refund.created_at.isoformat()
            )
            for agg in refund_aggs
        ]

        # Paginate
        total = len(summaries)
        start_idx = (query.page - 1) * query.page_size
        end_idx = start_idx + query.page_size
        paginated_items = summaries[start_idx:end_idx]
        total_pages = ceil(total / query.page_size) if total > 0 else 1

        return RefundListResponse(
            items=paginated_items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages
        )


class GetRefundByBookingQueryHandler:
    """
    Handler for GetRefundByBookingQuery.
    Retrieves refund for a specific booking.
    """

    def __init__(self, refund_repository: RefundRepository):
        """
        Initialize handler with refund repository.
        
        Args:
            refund_repository: RefundRepository instance
        """
        self.refund_repository = refund_repository

    def handle(self, query: GetRefundByBookingQuery) -> RefundDetailResponse:
        """
        Handle GetRefundByBookingQuery.
        
        Args:
            query: GetRefundByBookingQuery with booking_id
            
        Returns:
            RefundDetailResponse: Refund details
            
        Raises:
            ValueError: If refund not found
        """
        refund_agg = self.refund_repository.find_by_booking(query.booking_id)
        if not refund_agg:
            raise ValueError(f"No refund found for booking {query.booking_id}")

        refund = refund_agg.refund

        return RefundDetailResponse(
            refund_id=refund.refund_id,
            booking_id=refund.booking_id,
            customer_id=refund.customer_id,
            event_id=refund.event_id,
            refund_amount=refund.refund_amount.amount,
            status=str(refund.status),
            created_at=refund.created_at.isoformat(),
            refund_deadline=refund.refund_deadline.isoformat(),
            rejection_reason=refund.rejection_reason,
            payment_reference=refund.payment_reference,
            approved_at=refund.approved_at.isoformat() if refund.approved_at else None,
            rejected_at=refund.rejected_at.isoformat() if refund.rejected_at else None,
            paid_out_at=refund.paid_out_at.isoformat() if refund.paid_out_at else None,
        )


class GetApprovedRefundsQueryHandler:
    """
    Handler for GetApprovedRefundsQuery.
    Retrieves approved refunds pending payout (US18).
    """

    def __init__(self, refund_repository: RefundRepository):
        """
        Initialize handler with refund repository.
        
        Args:
            refund_repository: RefundRepository instance
        """
        self.refund_repository = refund_repository

    def handle(self, query: GetApprovedRefundsQuery) -> RefundListResponse:
        """
        Handle GetApprovedRefundsQuery.
        
        Args:
            query: GetApprovedRefundsQuery with pagination
            
        Returns:
            RefundListResponse: Paginated list of approved refunds
        """
        # Get approved refunds pending payout
        refund_aggs = self.refund_repository.find_approved_pending_payout()

        # Convert to summary DTOs
        summaries = [
            RefundSummaryResponse(
                refund_id=agg.refund.refund_id,
                booking_id=agg.refund.booking_id,
                refund_amount=agg.refund.refund_amount.amount,
                status=str(agg.refund.status),
                created_at=agg.refund.created_at.isoformat()
            )
            for agg in refund_aggs
        ]

        # Paginate
        total = len(summaries)
        start_idx = (query.page - 1) * query.page_size
        end_idx = start_idx + query.page_size
        paginated_items = summaries[start_idx:end_idx]
        total_pages = ceil(total / query.page_size) if total > 0 else 1

        return RefundListResponse(
            items=paginated_items,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages
        )
