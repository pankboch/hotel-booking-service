from collections.abc import Callable
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


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        pytest.param(
            lambda booking: booking.date_end,
            lambda booking: booking.date_end + timedelta(days=5),
            id="starts-on-existing-end-date",
        ),
        pytest.param(
            lambda booking: booking.date_start - timedelta(days=5),
            lambda booking: booking.date_start,
            id="ends-on-existing-start-date",
        ),
    ],
)
@pytest.mark.django_db
def test_create_booking_adjacent_dates_success(
    api_client: APIClient,
    booking: Booking,
    date_start: Callable[[Booking], date],
    date_end: Callable[[Booking], date],
) -> None:
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(
        booking.room.id,
        date_start=date_start(booking).isoformat(),
        date_end=date_end(booking).isoformat(),
    )

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    actual_data = response.json()
    assert "booking_id" in actual_data
    assert Booking.objects.count() == bookings_count_before + 1


@pytest.mark.parametrize("missing_field", ["room", "date_start", "date_end"])
@pytest.mark.django_db
def test_create_booking_without_required_fields(
    api_client: APIClient, room: Room, missing_field: str
) -> None:
    booking_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id)
    payload.pop(missing_field)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert missing_field in actual_data

    assert Booking.objects.count() == booking_count_before


@pytest.mark.parametrize(
    ("room_value", "expected_error"),
    [
        ("invalid_id", "Некорректный тип. Ожидалось значение первичного ключа, получен str."),
        ("", "Это поле не может быть пустым."),
    ],
)
@pytest.mark.django_db
def test_create_booking_with_invalid_room_value(
    api_client: APIClient, room: Room, room_value: str, expected_error: str
) -> None:
    booking_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id, room=room_value)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "room" in actual_data
    assert actual_data["room"] == [expected_error]

    assert Booking.objects.count() == booking_count_before


@pytest.mark.django_db
def test_create_booking_with_nonexistent_room(api_client: APIClient, room: Room) -> None:
    booking_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id, room=99999999)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "room" in actual_data

    assert Booking.objects.count() == booking_count_before


@pytest.mark.parametrize(
    ("date_start", "date_end", "invalid_fields"),
    [
        ("10.04.2026", "15.04.2026", ("date_start", "date_end")),
        ("2026/04/10", "2026/04/15", ("date_start", "date_end")),
        ("invalid", "2026-04-15", ("date_start",)),
        ("2026-04-10", "invalid", ("date_end",)),
        ("invalid", "invalid", ("date_start", "date_end")),
    ],
)
@pytest.mark.django_db
def test_create_booking_with_invalid_date_format(
    api_client: APIClient,
    room: Room,
    date_start: str,
    date_end: str,
    invalid_fields: tuple[str, ...],
) -> None:
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id, date_start=date_start, date_end=date_end)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    for field in invalid_fields:
        assert field in actual_data

    assert Booking.objects.count() == bookings_count_before


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        (
            (date.today() - timedelta(days=1)).isoformat(),
            (date.today() + timedelta(days=5)).isoformat(),
        ),
        (
            (date.today() - timedelta(days=30)).isoformat(),
            (date.today() - timedelta(days=25)).isoformat(),
        ),
    ],
)
@pytest.mark.django_db
def test_create_booking_with_date_start_in_past(
    api_client: APIClient, room: Room, date_start: str, date_end: str
) -> None:
    expected_error = "Нельзя создать бронирование на прошедшую дату."
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id, date_start=date_start, date_end=date_end)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "non_field_errors" in actual_data
    assert actual_data["non_field_errors"] == [expected_error]

    assert Booking.objects.count() == bookings_count_before


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        (
            (date.today() + timedelta(days=30)).isoformat(),
            (date.today() + timedelta(days=25)).isoformat(),
        ),
        (
            (date.today() + timedelta(days=30)).isoformat(),
            (date.today() + timedelta(days=30)).isoformat(),
        ),
    ],
)
@pytest.mark.django_db
def test_create_booking_with_date_end_before_date_start(
    api_client: APIClient, room: Room, date_start: str, date_end: str
) -> None:
    expected_error = "Дата начала бронирования должна быть раньше даты окончания."
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(room.id, date_start=date_start, date_end=date_end)

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "non_field_errors" in actual_data
    assert actual_data["non_field_errors"] == [expected_error]

    assert Booking.objects.count() == bookings_count_before


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        pytest.param(
            lambda booking: booking.date_start - timedelta(days=10),
            lambda booking: booking.date_start + timedelta(days=5),
            id="starts-before-existing-and-ends-inside",
        ),
        pytest.param(
            lambda booking: booking.date_start + timedelta(days=2),
            lambda booking: booking.date_end - timedelta(days=2),
            id="fully-inside-existing",
        ),
        pytest.param(
            lambda booking: booking.date_start + timedelta(days=5),
            lambda booking: booking.date_end + timedelta(days=10),
            id="starts-inside-existing-and-ends-after",
        ),
        pytest.param(
            lambda booking: booking.date_start - timedelta(days=5),
            lambda booking: booking.date_end + timedelta(days=5),
            id="fully-overlaps-existing",
        ),
    ],
)
@pytest.mark.django_db
def test_create_booking_with_overlapping_dates(
    api_client: APIClient,
    booking: Booking,
    date_start: Callable[[Booking], date],
    date_end: Callable[[Booking], date],
) -> None:
    expected_error = "Выбранные даты пересекаются с уже существующим бронированием."
    bookings_count_before = Booking.objects.count()
    payload = make_booking_payload(
        booking.room.id,
        date_start=date_start(booking).isoformat(),
        date_end=date_end(booking).isoformat(),
    )

    url = reverse("add_booking")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    actual_data = response.json()
    assert "non_field_errors" in actual_data
    assert actual_data["non_field_errors"] == [expected_error]

    assert Booking.objects.count() == bookings_count_before
