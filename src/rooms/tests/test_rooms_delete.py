from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bookings.models import Booking
from rooms.models import Room


@pytest.mark.django_db
def test_delete_room_without_bookings(api_client: APIClient, room: Room) -> None:
    url = reverse("delete_room", kwargs={"room_id": room.id})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["deleted_room"] == room.id
    assert actual["deleted_bookings"] == []
    assert not Room.objects.filter(id=room.id).exists()


@pytest.mark.django_db
def test_delete_room_with_bookings(api_client: APIClient, room_with_bookings: Room) -> None:
    room = room_with_bookings
    bookings_count = room.bookings.count()
    url = reverse("delete_room", kwargs={"room_id": room.id})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["deleted_room"] == room.id
    assert len(actual["deleted_bookings"]) == bookings_count
    assert not Room.objects.filter(id=room.id).exists()

    assert not Booking.objects.filter(room_id=room.id).exists()
