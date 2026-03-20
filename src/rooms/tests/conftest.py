from datetime import date, timedelta
from typing import Any

import pytest

from bookings.models import Booking
from rooms.models import Room


@pytest.fixture
def room(db: Any) -> Room:
    return Room.objects.create(price=7500, description="Номер с видом на горы")


@pytest.fixture
def rooms(db: Any) -> list[Room]:
    rooms = []
    for n in range(5):
        room = Room.objects.create(price=1000 * (n + 1), description=f"Room №{n}")
        rooms.append(room)

    return rooms


@pytest.fixture
def room_with_bookings(db: Any, room: Room) -> Room:
    for i in range(3):
        Booking.objects.create(
            room=room,
            date_start=date.today() + timedelta(days=30 + i * 10),
            date_end=date.today() + timedelta(days=35 + i * 10),
        )
    return room
