from app.application.interfaces.notification_service import NotificationService


class MockNotificationService(NotificationService):
    """Mock notification service — prints to console."""

    def send(self, destination: str, message: str) -> None:
        print(f"[MockNotificationService] To: {destination} | Message: {message}")
