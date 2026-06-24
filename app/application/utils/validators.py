
from typing import Any, Optional
from datetime import datetime

from app.domain.constants import ValidationMessages, ErrorMessages


class DomainValidator:
    
    @staticmethod
    def validate_not_none(value: Any, field_name: str) -> None:
        if value is None:
            raise ValueError(f"{field_name} cannot be None")
    
    @staticmethod
    def validate_positive(value: float, field_name: str) -> None:
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
    
    @staticmethod
    def validate_non_negative(value: float, field_name: str) -> None:
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative")
    
    @staticmethod
    def validate_string_not_empty(value: str, field_name: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
    
    @staticmethod
    def validate_date_range(
        start_date: datetime,
        end_date: datetime,
        field_name: str = "Date range"
    ) -> None:
        if end_date <= start_date:
            raise ValueError(
                f"{field_name}: end date must be after start date"
            )
    
    @staticmethod
    def validate_future_date(
        date: datetime,
        field_name: str = "Date"
    ) -> None:
        if date <= datetime.now():
            raise ValueError(f"{field_name} must be in the future")
    
    @staticmethod
    def validate_quota(
        quota: int,
        capacity: int,
        field_name: str = "Quota"
    ) -> None:
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
        if current_status not in allowed_statuses:
            raise ValueError(
                f"Cannot {operation}: status is {current_status}, "
                f"must be one of {allowed_statuses}"
            )
    
    @staticmethod
    def validate_type(value: Any, expected_type: type, field_name: str) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )


class QueryValidator:
    
    @staticmethod
    def validate_pagination_params(page: int, page_size: int) -> None:
        if page < 1:
            raise ValueError("Page number must be >= 1")
        
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        if page_size > 1000:
            raise ValueError("Page size cannot exceed 1000")
