from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from rooms.models import Room

from .models import Booking
from .serializers import BookingsRoomSerializer


class BookingsRoomGetView(generics.ListAPIView):
    """
    Представление для обработки GET-запроса.
    Из /bookings/room/<int:room_id>/ берет room_id
    и возвращает все брони, привязанные к этому номеру
    """

    serializer_class = BookingsRoomSerializer

    def get_room(self) -> Room:
        room_id = self.kwargs.get("room_id")
        return get_object_or_404(Room, id=room_id)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        room = self.get_room()
        bookings = Booking.objects.filter(room=room)
        serializer = self.get_serializer(bookings, many=True)

        return Response(
            data={"room_id": room.id, "bookings": serializer.data}, status=status.HTTP_200_OK
        )
