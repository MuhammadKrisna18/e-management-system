from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.repositories.in_memory_booking_repository import (
    InMemoryBookingRepository,
)
from app.infrastructure.repositories.in_memory_ticket_repository import (
    InMemoryTicketRepository,
)
from app.infrastructure.repositories.in_memory_refund_repository import (
    InMemoryRefundRepository,
)
from app.infrastructure.external_services.mock_payment_gateway import (
    MockPaymentGatewayService,
)
from app.infrastructure.external_services.mock_notification_service import (
    MockNotificationService,
)
from app.infrastructure.external_services.mock_refund_payment_service import (
    MockRefundPaymentService,
)


class RepositoryFactory:

    @staticmethod
    def create_event_repository():
        return InMemoryEventRepository()

    @staticmethod
    def create_booking_repository():
        return InMemoryBookingRepository()

    @staticmethod
    def create_ticket_repository():
        return InMemoryTicketRepository()

    @staticmethod
    def create_refund_repository():
        return InMemoryRefundRepository()


class ServiceFactory:

    @staticmethod
    def create_payment_gateway_service():
        return MockPaymentGatewayService()

    @staticmethod
    def create_notification_service():
        return MockNotificationService()

    @staticmethod
    def create_refund_payment_service():
        return MockRefundPaymentService()
