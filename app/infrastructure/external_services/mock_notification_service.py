from typing import List
from app.application.interfaces.notification_service import NotificationService


class MockNotificationService(NotificationService):

    def __init__(self):
        self._notifications: List[dict] = []

    def send(self, destination: str, message: str):
        self._log_notification({
            "type": "generic",
            "destination": destination,
            "message": message
        })

    def send_booking_confirmation(
        self, customer_id: str, booking_id: str, total_price: float
    ) -> bool:
        self._log_notification({
            "type": "booking_confirmation",
            "customer_id": customer_id,
            "booking_id": booking_id,
            "total_price": total_price,
        })
        return True

    def send_payment_reminder(
        self, customer_id: str, booking_id: str, deadline: str
    ) -> bool:
        self._log_notification({
            "type": "payment_reminder",
            "customer_id": customer_id,
            "booking_id": booking_id,
            "deadline": deadline,
        })
        return True

    def send_ticket_issued(
        self, customer_id: str, ticket_codes: List[str]
    ) -> bool:
        self._log_notification({
            "type": "ticket_issued",
            "customer_id": customer_id,
            "ticket_codes": ticket_codes,
        })
        return True

    def send_event_cancellation_notice(
        self, customer_id: str, event_id: str, event_name: str
    ) -> bool:
        self._log_notification({
            "type": "event_cancellation",
            "customer_id": customer_id,
            "event_id": event_id,
            "event_name": event_name,
        })
        return True

    def send_refund_approval(
        self, customer_id: str, refund_id: str, refund_amount: float
    ) -> bool:
        self._log_notification({
            "type": "refund_approval",
            "customer_id": customer_id,
            "refund_id": refund_id,
            "refund_amount": refund_amount,
        })
        return True

    def send_refund_payout_confirmation(
        self, customer_id: str, refund_id: str, payout_date: str
    ) -> bool:
        self._log_notification({
            "type": "refund_payout",
            "customer_id": customer_id,
            "refund_id": refund_id,
            "payout_date": payout_date,
        })
        return True

    def send_check_in_confirmation(
        self, customer_id: str, ticket_code: str, event_name: str
    ) -> bool:
        self._log_notification({
            "type": "check_in_confirmation",
            "customer_id": customer_id,
            "ticket_code": ticket_code,
            "event_name": event_name,
        })
        return True

    def get_sent_notifications(self) -> List[dict]:
        return self._notifications.copy()

    def _log_notification(self, notification: dict) -> None:
        self._notifications.append(notification)
        print(f"[NOTIFICATION] {notification}")
