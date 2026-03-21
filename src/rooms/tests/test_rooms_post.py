from decimal import Decimal

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from rooms.models import Room


@pytest.mark.parametrize(
    ("payload", "expected_price"),
    [
        (  # целое число
            {"price": 6500, "description": "Номер с видом на море."},
            Decimal("6500.00"),
        ),
        (  # число с 2 знаками после запятой
            {"price": 7150.50, "description": "Номер с видом на море."},
            Decimal("7150.50"),
        ),
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


@pytest.mark.parametrize(
    "payload",
    [
        {  # отрицательная цена
            "price": -100,
            "description": "Номер с видом на море.",
        },
        {  # больше 2х знаков после запятой
            "price": 100.123,
            "description": "Номер с видом на море.",
        },
        {  # больше 10 цифр до запятой
            "price": 12345678910.50,
            "description": "Номер с видом на море.",
        },
        {  # не число
            "price": "invalid_price",
            "description": "Номер с видом на море.",
        },
    ],
)
@pytest.mark.django_db
def test_create_room_invalid_price(api_client: APIClient, payload: dict) -> None:
    count_room_before = Room.objects.count()
    url = reverse("add_new_room")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "price" in response.json()
    assert Room.objects.count() == count_room_before


@pytest.mark.parametrize(
    "payload",
    [
        {  # описание больше 255 символов
            "price": 100,
            "description": "A" * 256,
        },
    ],
)
@pytest.mark.django_db
def test_create_room_description_too_long(api_client: APIClient, payload: dict) -> None:
    url = reverse("add_new_room")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "description" in response.json()
    assert Room.objects.count() == 0


@pytest.mark.parametrize(
    ("payload", "missing_field"),
    [
        (  # Есть цена, нет описания
            {"price": 100},
            ["description"],
        ),
        (  # Есть описание, нет цены
            {"description": "Номер с видом на море."},
            ["price"],
        ),
        (  # Пустое тело
            {},
            ["price", "description"],
        ),
    ],
)
@pytest.mark.django_db
def test_create_room_missing_fields(
    api_client: APIClient, payload: dict, missing_field: list[str]
) -> None:
    count_room_before = Room.objects.count()
    url = reverse("add_new_room")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    for field in missing_field:
        assert field in data

    assert Room.objects.count() == count_room_before
