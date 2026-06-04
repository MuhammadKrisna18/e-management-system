"""
Validation Utilities

Common validation logic for handlers and entities.
"""

from typing import Any, Optional
from datetime import datetime

from app.domain.constants import ValidationMessages, ErrorMessages


class DomainValidator:
    """Utility class for domain validation."""
    
    @staticmethod
    def validate_not_none(value: Any, field_name: str) -> None:
        """
        Validate that value is not None.
        
        Args:
            value: Value to check
            field_name: Name of field for error message
            
        Raises:
            ValueError: If value is None
        """
        if value is None:
            raise ValueError(f"{field_name} cannot be None")
    
    @staticmethod
    def validate_positive(value: float, field_name: str) -> None:
        """
        Validate that value is positive (> 0).
        
        Args:
            value: Value to check
            field_name: Name of field for error message
            
        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
    
    @staticmethod
    def validate_non_negative(value: float, field_name: str) -> None:
        """
        Validate that value is non-negative (>= 0).
        
        Args:
            value: Value to check
            field_name: Name of field for error message
            
        Raises:
            ValueError: If value is negative
        """
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative")
    
    @staticmethod
    def validate_string_not_empty(value: str, field_name: str) -> None:
        """
        Validate that string is not empty.
        
        Args:
            value: String to check
            field_name: Name of field for error message
            
        Raises:
            ValueError: If string is empty
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
    
    @staticmethod
    def validate_date_range(
        start_date: datetime,
        end_date: datetime,
        field_name: str = "Date range"
    ) -> None:
        """
        Validate that end date is after start date.
        
        Args:
            start_date: Start datetime
            end_date: End datetime
            field_name: Name of fields for error message
            
        Raises:
            ValueError: If end date is before start date
        """
        if end_date <= start_date:
            raise ValueError(
                f"{field_name}: end date must be after start date"
            )
    
    @staticmethod
    def validate_future_date(
        date: datetime,
        field_name: str = "Date"
    ) -> None:
        """
        Validate that date is in the future.
        
        Args:
            date: Date to check
            field_name: Name of field for error message
            
        Raises:
            ValueError: If date is not in future
        """
        if date <= datetime.now():
            raise ValueError(f"{field_name} must be in the future")
    
    @staticmethod
    def validate_quota(
        quota: int,
        capacity: int,
        field_name: str = "Quota"
    ) -> None:
        """
        Validate that quota does not exceed capacity.
        
        Args:
            quota: Quota value
            capacity: Maximum capacity
            field_name: Name of field for error message
            
        Raises:
            ValueError: If quota exceeds capacity
        """
        if quota > capacity:
            raise ValueError(
                f"{field_name} ({quota}) exceeds capacity ({capacity})"
            )
    
    @staticmethod
    def validate_status_transition(
        current_status: str,
        allowed_statuses: list,
        operation: str
    ) -> None:
        """
        Validate that current status allows operation.
        
        Args:
            current_status: Current status value
            allowed_statuses: List of allowed status values
            operation: Name of operation for error message
            
        Raises:
            ValueError: If current status not in allowed list
        """
        if current_status not in allowed_statuses:
            raise ValueError(
                f"Cannot {operation}: status is {current_status}, "
                f"must be one of {allowed_statuses}"
            )
    
    @staticmethod
    def validate_type(value: Any, expected_type: type, field_name: str) -> None:
        """
        Validate that value is of expected type.
        
        Args:
            value: Value to check
            expected_type: Expected type
            field_name: Name of field for error message
            
        Raises:
            TypeError: If type doesn't match
        """
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )


class QueryValidator:
    """Utility class for query validation."""
    
    @staticmethod
    def validate_pagination_params(page: int, page_size: int) -> None:
        """
        Validate pagination parameters.
        
        Args:
            page: Page number
            page_size: Items per page
            
        Raises:
            ValueError: If parameters invalid
        """
        if page < 1:
            raise ValueError("Page number must be >= 1")
        
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        if page_size > 1000:
            raise ValueError("Page size cannot exceed 1000")
