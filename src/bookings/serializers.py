from datetime import date

from rest_framework import serializers

from rooms.models import Room

from .models import Booking


class BookingAddSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проверки входных данных для создания брони.
    Принимает на вход room, date_start, date_end
    """

    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    date_start = serializers.DateField(input_formats=["%Y-%m-%d"])
    date_end = serializers.DateField(input_formats=["%Y-%m-%d"])

    class Meta:
        model = Booking
        fields = ("room", "date_start", "date_end")

    def validate(self, attrs):
        room = attrs["room"]
        date_start = attrs["date_start"]
        date_end = attrs["date_end"]

        if date_start >= date_end:
            raise serializers.ValidationError(
                "Дата начала бронирования должна быть раньше даты окончания."
            )

        if date_start < date.today():
            raise serializers.ValidationError("Нельзя создать бронирование на прошедшую дату.")

        overlapping_bookings = Booking.objects.filter(
            room=room, date_start__lt=date_end, date_end__gt=date_start
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                "Выбранные даты пересекаются с уже существующим бронированием."
            )

        return attrs


class BookingDeleteSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода информации об удаленной брони
    """

    class Meta:
        model = Booking
        fields = "__all__"


class BookingsRoomSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода броней у комнаты
    """

    class Meta:
        model = Booking
        fields = ("id", "date_start", "date_end")
