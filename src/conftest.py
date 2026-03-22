from datetime import date, timedelta
from typing import Any

import pytest
from rest_framework.test import APIClient

from bookings.models import Booking
from rooms.models import Room


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def room(db: Any) -> Room:
    return Room.objects.create(price=7500, description="Номер с видом на горы")


@pytest.fixture
def room_with_bookings(db: Any, room: Room) -> Room:
    for i in range(3):
        Booking.objects.create(
            room=room,
            date_start=date.today() + timedelta(days=30 + i * 10),
            date_end=date.today() + timedelta(days=35 + i * 10),
        )
    return room
