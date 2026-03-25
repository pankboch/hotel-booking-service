from datetime import date, timedelta
from typing import Any

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bookings.models import Booking
from bookings.serializers import BookingAddSerializer
from rooms.models import Room


def make_booking_payload(room_id: int, **overrides: Any) -> dict:
    payload = {
        "room": room_id,
        "date_start": (date.today() + timedelta(days=30)).isoformat(),
        "date_end": (date.today() + timedelta(days=35)).isoformat(),
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
def test_create_booking_success(api_client: APIClient, room: Room) -> None:
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id)

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


@pytest.mark.django_db
def test_create_booking_allows_same_dates_for_different_room(
    api_client: APIClient,
    booking: Booking,
    another_room: Room,
) -> None:
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(
        another_room.id,
        date_start=booking.date_start.isoformat(),
        date_end=booking.date_end.isoformat(),
    )

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    actual_data = response.json()
    assert "booking_id" in actual_data
    assert Booking.objects.count() == bookings_count_before + 1


@pytest.mark.django_db
def test_create_booking_allows_non_overlapping_dates(
    api_client: APIClient,
    booking: Booking,
) -> None:
    booking_count_before = Booking.objects.count()
    payload = make_booking_payload(
        booking.room.id,
        date_start=(booking.date_end + timedelta(days=1)).isoformat(),
        date_end=(booking.date_end + timedelta(days=5)).isoformat(),
    )

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    actual_data = response.json()
    assert "booking_id" in actual_data
    assert Booking.objects.count() == booking_count_before + 1
