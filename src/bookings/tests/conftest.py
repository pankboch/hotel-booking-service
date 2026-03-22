from datetime import date, timedelta
from typing import Any

import pytest

from bookings.models import Booking
from rooms.models import Room


@pytest.fixture
def booking(db: Any, room: Room) -> Booking:
    return Booking.objects.create(
        room=room,
        date_start=date.today() + timedelta(days=30),
        date_end=date.today() + timedelta(days=35),
    )
