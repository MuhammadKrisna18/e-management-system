from app.application.interfaces.notification_service import NotificationServiceInterface

class MockNotificationService(NotificationServiceInterface):
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        print(f"[MockNotificationService] Sending Email to {recipient}")
        print(f"  Subject: {subject}")
        print(f"  Body: {body}")
