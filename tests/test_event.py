import pytest
from datetime import datetime
from app.domain.entities.event import Event


def test_event_invalid_date():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 10),
            datetime(2025, 10, 1),
            100
        )


def test_event_invalid_capacity():
    with pytest.raises(ValueError):
        Event(
            "Test Event",
            datetime(2025, 10, 1),
            datetime(2025, 10, 10),
            0
        )