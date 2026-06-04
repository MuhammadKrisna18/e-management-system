"""Infrastructure Configuration and Dependency Injection"""
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
    """Factory for creating repository instances."""

    @staticmethod
    def create_event_repository():
        """Create event repository instance."""
        return InMemoryEventRepository()

    @staticmethod
    def create_booking_repository():
        """Create booking repository instance."""
        return InMemoryBookingRepository()

    @staticmethod
    def create_ticket_repository():
        """Create ticket repository instance."""
        return InMemoryTicketRepository()

    @staticmethod
    def create_refund_repository():
        """Create refund repository instance."""
        return InMemoryRefundRepository()


class ServiceFactory:
    """Factory for creating external service instances."""

    @staticmethod
    def create_payment_gateway_service():
        """Create payment gateway service instance."""
        return MockPaymentGatewayService()

    @staticmethod
    def create_notification_service():
        """Create notification service instance."""
        return MockNotificationService()

    @staticmethod
    def create_refund_payment_service():
        """Create refund payment service instance."""
        return MockRefundPaymentService()
