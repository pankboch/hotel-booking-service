from datetime import timedelta
from typing import Any

from django.utils import timezone
import pytest

from rooms.models import Room


@pytest.fixture
def rooms(db: Any) -> list[Room]:
    rooms = []

    for n in range(5):
        room = Room.objects.create(price=1000 * (n + 1), description=f"Room №{n}")
        Room.objects.filter(id=room.id).update(created_at=timezone.now() + timedelta(minutes=n))

        room.refresh_from_db()
        rooms.append(room)

    return rooms
