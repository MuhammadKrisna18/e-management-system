
from app.infrastructure.repositories.postgres_event_repository import PostgresEventRepository
from app.infrastructure.repositories.postgres_booking_repository import PostgresBookingRepository
from app.infrastructure.repositories.postgres_refund_repository import PostgresRefundRepository
from app.infrastructure.repositories.postgres_ticket_repository import PostgresTicketRepository
from app.infrastructure.database.database import SessionLocal

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
from app.application.command_handlers.cancel_event_handler import (
    CancelEventHandler
)
from app.application.command_handlers.create_ticket_category_handler import (
    CreateTicketCategoryHandler
)
from app.application.command_handlers.disable_ticket_category_handler import (
    DisableTicketCategoryHandler
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
from app.application.command_handlers.check_in_ticket_handler import (
    CheckInTicketHandler
)
from app.application.command_handlers.expire_booking_handler import (
    ExpireBookingHandler
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

    def __init__(self, db_session=None):
        # Initialize session
        self.db_session = db_session or SessionLocal()
        
        # Initialize repositories (singleton instances)
        self.event_repository = PostgresEventRepository(self.db_session)
        self.booking_repository = PostgresBookingRepository(self.db_session)
        self.refund_repository = PostgresRefundRepository(self.db_session)
        self.ticket_repository = PostgresTicketRepository(self.db_session)

        # Initialize external services (singleton instances)
        self.payment_gateway = MockPaymentGatewayService()
        self.refund_payment_service = MockRefundPaymentService()
        self.notification_service = MockNotificationService()

        # Initialize command handlers (created on demand)
        self._create_event_handler = None
        self._cancel_event_handler = None
        self._create_ticket_category_handler = None
        self._disable_ticket_category_handler = None
        self._publish_event_handler = None
        self._create_booking_handler = None
        self._pay_booking_handler = None
        self._request_refund_handler = None
        self._approve_refund_handler = None
        self._reject_refund_handler = None
        self._mark_refund_payout_handler = None
        self._check_in_ticket_handler = None
        self._expire_booking_handler = None

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
        if self._create_event_handler is None:
            self._create_event_handler = CreateEventHandler(self.event_repository)
        return self._create_event_handler

    def get_cancel_event_handler(self) -> CancelEventHandler:
        if self._cancel_event_handler is None:
            self._cancel_event_handler = CancelEventHandler(self.event_repository)
        return self._cancel_event_handler

    def get_create_ticket_category_handler(self) -> CreateTicketCategoryHandler:
        if self._create_ticket_category_handler is None:
            self._create_ticket_category_handler = CreateTicketCategoryHandler(self.event_repository)
        return self._create_ticket_category_handler

    def get_disable_ticket_category_handler(self) -> DisableTicketCategoryHandler:
        if self._disable_ticket_category_handler is None:
            self._disable_ticket_category_handler = DisableTicketCategoryHandler(self.event_repository)
        return self._disable_ticket_category_handler

    def get_publish_event_handler(self) -> PublishEventHandler:
        if self._publish_event_handler is None:
            self._publish_event_handler = PublishEventHandler(self.event_repository)
        return self._publish_event_handler

    def get_create_booking_handler(self) -> CreateBookingHandler:
        if self._create_booking_handler is None:
            self._create_booking_handler = CreateBookingHandler(
                self.booking_repository,
                self.event_repository
            )
        return self._create_booking_handler

    def get_pay_booking_handler(self) -> PayBookingHandler:
        if self._pay_booking_handler is None:
            self._pay_booking_handler = PayBookingHandler(
                self.booking_repository,
                self.payment_gateway
            )
        return self._pay_booking_handler

    def get_request_refund_handler(self) -> RequestRefundHandler:
        if self._request_refund_handler is None:
            self._request_refund_handler = RequestRefundHandler(
                self.booking_repository,
                self.refund_repository
            )
        return self._request_refund_handler

    def get_approve_refund_handler(self) -> ApproveRefundHandler:
        if self._approve_refund_handler is None:
            self._approve_refund_handler = ApproveRefundHandler(
                self.refund_repository,
                self.booking_repository
            )
        return self._approve_refund_handler

    def get_reject_refund_handler(self) -> RejectRefundHandler:
        if self._reject_refund_handler is None:
            self._reject_refund_handler = RejectRefundHandler(
                self.refund_repository
            )
        return self._reject_refund_handler

    def get_mark_refund_payout_handler(self) -> MarkRefundPayoutHandler:
        if self._mark_refund_payout_handler is None:
            self._mark_refund_payout_handler = MarkRefundPayoutHandler(
                self.refund_repository,
                self.refund_payment_service
            )
        return self._mark_refund_payout_handler

    def get_check_in_ticket_handler(self) -> CheckInTicketHandler:
        if self._check_in_ticket_handler is None:
            self._check_in_ticket_handler = CheckInTicketHandler(
                self.ticket_repository,
                self.event_repository
            )
        return self._check_in_ticket_handler

    def get_expire_booking_handler(self) -> ExpireBookingHandler:
        if self._expire_booking_handler is None:
            self._expire_booking_handler = ExpireBookingHandler(
                self.booking_repository
            )
        return self._expire_booking_handler

    # Query Handlers

    def get_available_events_handler(self) -> GetAvailableEventsHandler:
        if self._get_available_events_handler is None:
            self._get_available_events_handler = GetAvailableEventsHandler(
                self.event_repository
            )
        return self._get_available_events_handler

    def get_event_details_handler(self) -> GetEventDetailsHandler:
        if self._get_event_details_handler is None:
            self._get_event_details_handler = GetEventDetailsHandler(
                self.event_repository
            )
        return self._get_event_details_handler

    def get_refund_details_handler(self) -> GetRefundDetailsQueryHandler:
        if self._get_refund_details_handler is None:
            self._get_refund_details_handler = GetRefundDetailsQueryHandler(
                self.refund_repository
            )
        return self._get_refund_details_handler

    def get_customer_refunds_handler(self) -> GetCustomerRefundsQueryHandler:
        if self._get_customer_refunds_handler is None:
            self._get_customer_refunds_handler = GetCustomerRefundsQueryHandler(
                self.refund_repository
            )
        return self._get_customer_refunds_handler

    def get_approved_refunds_handler(self) -> GetApprovedRefundsQueryHandler:
        if self._get_approved_refunds_handler is None:
            self._get_approved_refunds_handler = GetApprovedRefundsQueryHandler(
                self.refund_repository
            )
        return self._get_approved_refunds_handler

    def get_event_sales_report_handler(self) -> GetEventSalesReportQueryHandler:
        if self._get_event_sales_report_handler is None:
            self._get_event_sales_report_handler = GetEventSalesReportQueryHandler(
                self.event_repository,
                self.booking_repository,
                self.ticket_repository
            )
        return self._get_event_sales_report_handler

    def get_event_participants_handler(self) -> GetEventParticipantsQueryHandler:
        if self._get_event_participants_handler is None:
            self._get_event_participants_handler = GetEventParticipantsQueryHandler(
                self.event_repository,
                self.booking_repository,
                self.ticket_repository
            )
        return self._get_event_participants_handler

    def get_purchased_tickets_handler(self):
        from app.application.query_handlers.ticket_query_handlers import GetPurchasedTicketsQueryHandler
        if not hasattr(self, '_get_purchased_tickets_handler') or self._get_purchased_tickets_handler is None:
            self._get_purchased_tickets_handler = GetPurchasedTicketsQueryHandler(
                self.booking_repository,
                self.ticket_repository,
                self.event_repository
            )
        return self._get_purchased_tickets_handler

    # Utility methods

    def clear_all_data(self):
        # Only useful for tests if we want to reset; in production with Postgres we'd truncate tables
        self.event_repository = PostgresEventRepository(self.db_session)
        self.booking_repository = PostgresBookingRepository(self.db_session)
        self.refund_repository = PostgresRefundRepository(self.db_session)
        self.ticket_repository = PostgresTicketRepository(self.db_session)

    def reset_handlers(self):
        self._create_event_handler = None
        self._cancel_event_handler = None
        self._create_ticket_category_handler = None
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
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container():
    global _container
    _container = None
