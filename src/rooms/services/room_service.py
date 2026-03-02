from django.db.models import QuerySet

from rooms.models import Room


class RoomService:
    @staticmethod
    def create_room(price: int, description: str) -> Room:
        return Room.objects.create(description=description, price=price)

    @staticmethod
    def delete_room(room_id: int) -> dict:
        room = Room.objects.get(id=room_id)

        bookings_data = RoomService._get_bookings_for_room(room)
        room.delete()

        return {"deleted_room": room_id, "deleted_bookings": bookings_data}

    @staticmethod
    def get_rooms() -> QuerySet[Room]:  # надо добавить сортировку по цене и дате добавления
        return Room.objects.all()

    @staticmethod
    def _get_bookings_for_room(room: Room) -> list[dict] | list:
        bookings = room.bookings.all()
        bookings_data = [
            {"id": booking.pk, "date_start": booking.date_start, "date_end": booking.date_end}
            for booking in bookings
        ]

        return bookings_data
