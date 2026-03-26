from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from bookings.serializers import BookingsRoomSerializer
from rooms.models import Room


def assert_room_bookings_response(response: Response, expected_room: Room) -> None:
    """Вспомогательный метод для проверки успешного получения списка броней."""
    assert response.status_code == status.HTTP_200_OK

    actual_data = response.json()

    assert "room_id" in actual_data
    assert actual_data["room_id"] == expected_room.id

    assert "bookings" in actual_data
    assert isinstance(actual_data["bookings"], list)

    expected_bookings = BookingsRoomSerializer(expected_room.bookings.all(), many=True).data
    actual_bookings = actual_data["bookings"]
    assert actual_bookings == expected_bookings


@pytest.mark.django_db
def test_get_bookings_for_room_with_bookings(
    api_client: APIClient, room_with_bookings: Room
) -> None:
    url = reverse("all_bookings_for_room") + f"?room_id={room_with_bookings.id}"
    response = api_client.get(url)
    assert_room_bookings_response(response, room_with_bookings)


@pytest.mark.django_db
def test_get_bookings_for_room_without_bookings(api_client: APIClient, room: Room) -> None:
    url = reverse("all_bookings_for_room") + f"?room_id={room.id}"
    response = api_client.get(url)
    assert_room_bookings_response(response, room)


@pytest.mark.django_db
def test_get_bookings_for_room_invalid_not_found(api_client: APIClient) -> None:
    url = reverse("all_bookings_for_room") + "?room_id=9999999999"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    ("params", "expected_error"),
    [
        ({"room_id": "invalid_id"}, "Параметр room_id должен быть целым числом."),
        ({"room_id": ""}, "Параметр room_id должен быть целым числом."),
        ({}, "Параметр room_id обязателен."),
    ],
)
@pytest.mark.django_db
def test_get_bookings_for_room_invalid_or_missing_room_id(
    api_client: APIClient, params: dict, expected_error: str
) -> None:
    url = reverse("all_bookings_for_room")
    response = api_client.get(url, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "room_id" in actual_data
    assert actual_data["room_id"] == expected_error
