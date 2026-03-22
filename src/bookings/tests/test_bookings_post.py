from datetime import date, timedelta

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bookings.models import Booking
from bookings.serializers import BookingAddSerializer
from rooms.models import Room


@pytest.mark.django_db
def test_create_booking_success(api_client: APIClient, room: Room) -> None:
    bookings_count_before = Booking.objects.count()
    payload = {
        "room": room.id,
        "date_start": (date.today() + timedelta(days=30)).isoformat(),
        "date_end": (date.today() + timedelta(days=35)).isoformat(),
    }

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    actual_data = response.json()
    assert "booking_id" in actual_data
    assert isinstance(actual_data["booking_id"], int)

    assert Booking.objects.count() == bookings_count_before + 1

    created_booking = Booking.objects.get(id=actual_data["booking_id"])
    actual_booking = BookingAddSerializer(created_booking).data
    assert actual_booking == payload
