"""
Dependency Injection Container

Configures all application services, repositories, and handlers.
Provides a central point for managing object creation and wiring.
"""

from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository
)
from app.infrastructure.repositories.in_memory_booking_repository import (
    InMemoryBookingRepository
)
from app.infrastructure.repositories.in_memory_refund_repository import (
    InMemoryRefundRepository
)
from app.infrastructure.repositories.in_memory_ticket_repository import (
    InMemoryTicketRepository
)

from app.infrastructure.external_services.mock_payment_gateway import (
    MockPaymentGatewayService
)
from app.infrastructure.external_services.mock_refund_payment_service import (
    MockRefundPaymentService
)
from app.infrastructure.external_services.mock_notification_service import (
    MockNotificationService
)

# Command Handlers
from app.application.command_handlers.create_event_handler import (
    CreateEventHandler
)
from app.application.command_handlers.publish_event_handler import (
    PublishEventHandler
)
from app.application.command_handlers.create_booking_handler import (
    CreateBookingHandler
)
from app.application.command_handlers.pay_booking_handler import (
    PayBookingHandler
)
from app.application.command_handlers.request_refund_handler import (
    RequestRefundHandler
)
from app.application.command_handlers.approve_refund_handler import (
    ApproveRefundHandler
)
from app.application.command_handlers.reject_refund_handler import (
    RejectRefundHandler
)
from app.application.command_handlers.mark_refund_payout_handler import (
    MarkRefundPayoutHandler
)

# Query Handlers
from app.application.query_handlers.get_available_events_handler import (
    GetAvailableEventsHandler
)
from app.application.query_handlers.get_event_details_handler import (
    GetEventDetailsHandler
)
from app.application.query_handlers.refund_query_handlers import (
    GetRefundDetailsQueryHandler,
    GetCustomerRefundsQueryHandler,
    GetApprovedRefundsQueryHandler
)
from app.application.query_handlers.report_query_handlers import (
    GetEventSalesReportQueryHandler,
    GetEventParticipantsQueryHandler
)


class Container:
    """
    Central dependency injection container.
    
    Manages creation and configuration of all application components.
    Supports both lazy initialization and singleton patterns.
    """

    def __init__(self):
        """Initialize container with all repositories and services."""
        # Initialize repositories (singleton instances)
        self.event_repository = InMemoryEventRepository()
        self.booking_repository = InMemoryBookingRepository()
        self.refund_repository = InMemoryRefundRepository()
        self.ticket_repository = InMemoryTicketRepository()

        # Initialize external services (singleton instances)
        self.payment_gateway = MockPaymentGatewayService()
        self.refund_payment_service = MockRefundPaymentService()
        self.notification_service = MockNotificationService()

        # Initialize command handlers (created on demand)
        self._create_event_handler = None
        self._publish_event_handler = None
        self._create_booking_handler = None
        self._pay_booking_handler = None
        self._request_refund_handler = None
        self._approve_refund_handler = None
        self._reject_refund_handler = None
        self._mark_refund_payout_handler = None

        # Initialize query handlers (created on demand)
        self._get_available_events_handler = None
        self._get_event_details_handler = None
        self._get_refund_details_handler = None
        self._get_customer_refunds_handler = None
        self._get_approved_refunds_handler = None
        self._get_event_sales_report_handler = None
        self._get_event_participants_handler = None

    # Command Handlers

    def get_create_event_handler(self) -> CreateEventHandler:
        """Get CreateEventHandler instance."""
        if self._create_event_handler is None:
            self._create_event_handler = CreateEventHandler(self.event_repository)
        return self._create_event_handler

    def get_publish_event_handler(self) -> PublishEventHandler:
        """Get PublishEventHandler instance."""
        if self._publish_event_handler is None:
            self._publish_event_handler = PublishEventHandler(self.event_repository)
        return self._publish_event_handler

    def get_create_booking_handler(self) -> CreateBookingHandler:
        """Get CreateBookingHandler instance."""
        if self._create_booking_handler is None:
            self._create_booking_handler = CreateBookingHandler(
                self.booking_repository
            )
        return self._create_booking_handler

    def get_pay_booking_handler(self) -> PayBookingHandler:
        """Get PayBookingHandler instance."""
        if self._pay_booking_handler is None:
            self._pay_booking_handler = PayBookingHandler(
                self.booking_repository,
                self.payment_gateway
            )
        return self._pay_booking_handler

    def get_request_refund_handler(self) -> RequestRefundHandler:
        """Get RequestRefundHandler instance."""
        if self._request_refund_handler is None:
            self._request_refund_handler = RequestRefundHandler(
                self.booking_repository,
                self.refund_repository
            )
        return self._request_refund_handler

    def get_approve_refund_handler(self) -> ApproveRefundHandler:
        """Get ApproveRefundHandler instance."""
        if self._approve_refund_handler is None:
            self._approve_refund_handler = ApproveRefundHandler(
                self.refund_repository,
                self.booking_repository
            )
        return self._approve_refund_handler

    def get_reject_refund_handler(self) -> RejectRefundHandler:
        """Get RejectRefundHandler instance."""
        if self._reject_refund_handler is None:
            self._reject_refund_handler = RejectRefundHandler(
                self.refund_repository
            )
        return self._reject_refund_handler

    def get_mark_refund_payout_handler(self) -> MarkRefundPayoutHandler:
        """Get MarkRefundPayoutHandler instance."""
        if self._mark_refund_payout_handler is None:
            self._mark_refund_payout_handler = MarkRefundPayoutHandler(
                self.refund_repository,
                self.refund_payment_service
            )
        return self._mark_refund_payout_handler

    # Query Handlers

    def get_available_events_handler(self) -> GetAvailableEventsHandler:
        """Get GetAvailableEventsHandler instance."""
        if self._get_available_events_handler is None:
            self._get_available_events_handler = GetAvailableEventsHandler(
                self.event_repository
            )
        return self._get_available_events_handler

    def get_event_details_handler(self) -> GetEventDetailsHandler:
        """Get GetEventDetailsHandler instance."""
        if self._get_event_details_handler is None:
            self._get_event_details_handler = GetEventDetailsHandler(
                self.event_repository
            )
        return self._get_event_details_handler

    def get_refund_details_handler(self) -> GetRefundDetailsQueryHandler:
        """Get GetRefundDetailsQueryHandler instance."""
        if self._get_refund_details_handler is None:
            self._get_refund_details_handler = GetRefundDetailsQueryHandler(
                self.refund_repository
            )
        return self._get_refund_details_handler

    def get_customer_refunds_handler(self) -> GetCustomerRefundsQueryHandler:
        """Get GetCustomerRefundsQueryHandler instance."""
        if self._get_customer_refunds_handler is None:
            self._get_customer_refunds_handler = GetCustomerRefundsQueryHandler(
                self.refund_repository
            )
        return self._get_customer_refunds_handler

    def get_approved_refunds_handler(self) -> GetApprovedRefundsQueryHandler:
        """Get GetApprovedRefundsQueryHandler instance."""
        if self._get_approved_refunds_handler is None:
            self._get_approved_refunds_handler = GetApprovedRefundsQueryHandler(
                self.refund_repository
            )
        return self._get_approved_refunds_handler

    def get_event_sales_report_handler(self) -> GetEventSalesReportQueryHandler:
        """Get GetEventSalesReportQueryHandler instance."""
        if self._get_event_sales_report_handler is None:
            self._get_event_sales_report_handler = GetEventSalesReportQueryHandler(
                self.event_repository,
                self.booking_repository,
                self.ticket_repository
            )
        return self._get_event_sales_report_handler

    def get_event_participants_handler(self) -> GetEventParticipantsQueryHandler:
        """Get GetEventParticipantsQueryHandler instance."""
        if self._get_event_participants_handler is None:
            self._get_event_participants_handler = GetEventParticipantsQueryHandler(
                self.event_repository,
                self.booking_repository,
                self.ticket_repository
            )
        return self._get_event_participants_handler

    # Utility methods

    def clear_all_data(self):
        """
        Clear all repositories (useful for testing).
        Resets all in-memory storage to initial state.
        """
        self.event_repository = InMemoryEventRepository()
        self.booking_repository = InMemoryBookingRepository()
        self.refund_repository = InMemoryRefundRepository()
        self.ticket_repository = InMemoryTicketRepository()

    def reset_handlers(self):
        """Reset all cached handler instances."""
        self._create_event_handler = None
        self._publish_event_handler = None
        self._create_booking_handler = None
        self._pay_booking_handler = None
        self._request_refund_handler = None
        self._approve_refund_handler = None
        self._reject_refund_handler = None
        self._mark_refund_payout_handler = None
        self._get_available_events_handler = None
        self._get_event_details_handler = None
        self._get_refund_details_handler = None
        self._get_customer_refunds_handler = None
        self._get_approved_refunds_handler = None
        self._get_event_sales_report_handler = None
        self._get_event_participants_handler = None


# Global container instance
_container = None


def get_container() -> Container:
    """
    Get or create global container instance.
    
    Returns:
        Container: The global dependency injection container
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container():
    """Reset the global container instance."""
    global _container
    _container = None
