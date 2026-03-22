from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bookings.serializers import BookingsRoomSerializer
from rooms.models import Room


def assert_room_bookings_response(api_client: APIClient, expected_room: Room) -> None:
    url = reverse("all_bookings_for_room") + f"?room_id={expected_room.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual_data = response.json()
    assert isinstance(actual_data, dict)

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
    assert_room_bookings_response(api_client, room_with_bookings)


@pytest.mark.django_db
def test_get_bookings_for_room_without_bookings(api_client: APIClient, room: Room) -> None:
    assert_room_bookings_response(api_client, room)
