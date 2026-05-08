"""Notification Service Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class NotificationService(ABC):
    """Interface for notification service"""

    @abstractmethod
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: str = None,
    ) -> Dict[str, Any]:
        """
        Send email notification
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body (plain text)
            html_body: Email body (HTML)
            
        Returns:
            Dictionary with result {success, message_id}
        """
        pass

    @abstractmethod
    def send_sms(
        self,
        phone: str,
        message: str,
    ) -> Dict[str, Any]:
        """
        Send SMS notification
        
        Args:
            phone: Recipient phone number
            message: SMS message
            
        Returns:
            Dictionary with result {success, message_id}
        """
        pass

    @abstractmethod
    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
    ) -> Dict[str, Any]:
        """
        Send bulk email notification
        
        Args:
            recipients: List of recipient emails
            subject: Email subject
            body: Email body
            
        Returns:
            Dictionary with result {success, sent_count, failed_count}
        """
        pass
