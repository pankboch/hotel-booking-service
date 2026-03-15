from datetime import date
from typing import Any

from rest_framework import filters, generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Room
from .serializers import RoomCreateSerializer, RoomGetSerializer


class RoomCreateView(generics.CreateAPIView):
    """
    Представление для обработки POST-запроса.
    Принимает description и price и создает новую комнату.
    Возвращает id созданной комнаты.
    """

    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_room = serializer.save()

        return Response({"new_room_id": new_room.id}, status=status.HTTP_201_CREATED)


class RoomDeleteView(generics.DestroyAPIView):
    """
    Представление для обработки DELETE-запроса.
    Из url http://127.0.0.1:8000/rooms/delete/<int:room_id>/ берет room_id.
    Удаляет соответствующую комнату и брони для этой комнаты.
    """

    queryset = Room.objects.all()
    lookup_url_kwarg = "room_id"

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        room_id = instance.id
        bookings: list[dict[str, int | date]] = [
            {
                "booking_id": booking.id,
                "date_start": booking.date_start,
                "date_end": booking.date_end,
            }
            for booking in instance.bookings.all()
        ]
        self.perform_destroy(instance)

        return Response(
            {"deleted_room": room_id, "deleted_bookings": bookings}, status=status.HTTP_200_OK
        )


class RoomGetView(generics.ListAPIView):
    """
    Представление для обработки GET-запроса.
    Возвращает список всех комнат.
    Можно отфильтровать по цене или описанию.
    """

    queryset = Room.objects.all()
    serializer_class = RoomGetSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "description"]
