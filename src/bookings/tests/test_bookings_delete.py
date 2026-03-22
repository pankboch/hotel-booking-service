from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bookings.models import Booking
from bookings.serializers import BookingDeleteSerializer


@pytest.mark.django_db
def test_delete_booking_success(api_client: APIClient, booking: Booking) -> None:
    url = reverse("delete_booking", kwargs={"booking_id": booking.id})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()
    assert "deleted_booking" in actual

    expected_booking = BookingDeleteSerializer(booking).data
    assert actual["deleted_booking"] == expected_booking

    assert not Booking.objects.filter(id=booking.id).exists()
