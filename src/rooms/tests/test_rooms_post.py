from decimal import Decimal

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from rooms.models import Room


@pytest.mark.parametrize(
    ("payload", "expected_price"),
    [
        ({"price": 6500, "description": "Номер с видом на море."}, Decimal("6500.00")),
        ({"price": 7150.50, "description": "Номер с видом на море."}, Decimal("7150.50")),
    ],
)
@pytest.mark.django_db
def test_create_room_success(api_client: APIClient, payload: dict, expected_price: Decimal) -> None:
    url = reverse("add_new_room")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    actual = response.json()
    assert "new_room_id" in actual
    assert isinstance(actual["new_room_id"], int)

    room = Room.objects.get(id=actual["new_room_id"])
    assert room.price == expected_price
    assert room.description == payload["description"]
    assert room.created_at is not None
