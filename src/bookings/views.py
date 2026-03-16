from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from rooms.models import Room

from .models import Booking
from .serializers import BookingAddSerializer, BookingDeleteSerializer, BookingsRoomSerializer


class BookingAddView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingAddSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        return Response(data={"booking_id": booking.id}, status=status.HTTP_201_CREATED)


class BookingDeleteView(generics.DestroyAPIView):
    """
    Представление для обработки DELETE-запроса.
    Из /bookings/delete/<int:booking_id>/ берет booking_id
    и удаляет бронь
    """

    queryset = Booking.objects.all()
    serializer_class = BookingDeleteSerializer
    lookup_url_kwarg = "booking_id"

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        booking = self.get_object()
        serializer = self.get_serializer(booking)
        deleted_data = serializer.data
        self.perform_destroy(instance=booking)

        return Response(data={"deleted_booking": deleted_data}, status=status.HTTP_200_OK)


class BookingsRoomGetView(generics.ListAPIView):
    """
    Представление для обработки GET-запроса.
    Из /bookings/room/<int:room_id>/ берет room_id
    и возвращает все брони, привязанные к этому номеру
    """

    serializer_class = BookingsRoomSerializer

    def get_room(self) -> Room:
        room_id = self.request.query_params.get("room_id")
        if room_id is None:
            raise ValidationError({"room_id": "Параметр room_id обязателен."})
        return get_object_or_404(Room, id=room_id)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        room = self.get_room()
        bookings = Booking.objects.filter(room=room)
        serializer = self.get_serializer(bookings, many=True)

        return Response(
            data={"room_id": room.id, "bookings": serializer.data}, status=status.HTTP_200_OK
        )
