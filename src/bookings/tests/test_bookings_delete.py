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


@pytest.mark.django_db
def test_delete_booking_not_found(api_client: APIClient) -> None:
    url = reverse("delete_booking", kwargs={"booking_id": 99999999})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    actual = response.json()
    assert "detail" in actual


@pytest.mark.django_db
def test_delete_booking_does_not_delete_other_bookings(
    api_client: APIClient, booking: Booking, another_booking: Booking
) -> None:
    bookings_count_before = Booking.objects.count()
    url = reverse("delete_booking", kwargs={"booking_id": booking.id})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK

    assert not Booking.objects.filter(id=booking.id).exists()
    assert Booking.objects.filter(id=another_booking.id).exists()

    assert Booking.objects.count() == bookings_count_before - 1
