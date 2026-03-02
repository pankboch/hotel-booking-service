from datetime import date

from bookings.exceptions import (
    BookingNotFoundError,
    BookingOverlapError,
    InvalidDateRangeError,
    RoomNotFoundError,
)
from bookings.models import Booking
from rooms.models import Room


class BookingService:
    @staticmethod
    def create_booking(room_id: int, date_start: date, date_end: date) -> Booking:
        BookingService._check_room_exists(room_id)
        BookingService._validate_date_range(date_start, date_end)
        BookingService._check_no_overlapping_bookings(room_id, date_start, date_end)

        booking = Booking.objects.create(room_id=room_id, date_start=date_start, date_end=date_end)
        return booking

    @staticmethod
    def delete_booking(booking_id: int) -> dict:
        BookingService._check_booking_exists(booking_id)
        booking = Booking.objects.get(id=booking_id)
        data = {
            "deleted_booking": booking_id,
            "room_id": booking.room_id,
            "date_start": booking.date_start,
            "date_end": booking.date_end,
        }
        booking.delete()
        return data

    @staticmethod
    def get_bookings_for_room(room_id: int) -> list[dict] | list:
        BookingService._check_room_exists(room_id)
        bookings = Booking.objects.filter(room_id=room_id)
        bookings_data = [
            {
                "booking_id": booking.pk,
                "date_start": booking.date_start,
                "date_end": booking.date_end,
            }
            for booking in bookings
        ]
        return bookings_data

    @staticmethod
    def _check_room_exists(room_id: int) -> None:
        if not Room.objects.filter(id=room_id).exists():
            raise RoomNotFoundError(f"Комнаты {room_id} не существует")

    @staticmethod
    def _validate_date_range(date_start: date, date_end: date) -> None:
        if date_start >= date_end:
            raise InvalidDateRangeError("Дата начала должна быть меньше даты окончания")

    @staticmethod
    def _check_no_overlapping_bookings(room_id: int, date_start: date, date_end: date) -> None:
        if Booking.objects.filter(
            room_id=room_id, date_start__lt=date_end, date_end__gt=date_start
        ).exists():
            raise BookingOverlapError(
                "Невозможно создать бронь, так как она пересекается с существующими бронями для данной комнаты"
            )

    @staticmethod
    def _check_booking_exists(booking_id: int) -> None:
        if not Booking.objects.filter(id=booking_id).exists():
            raise BookingNotFoundError(f"Брони {booking_id} не существует")
