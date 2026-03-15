from rest_framework import serializers

from .models import Booking


class BookingsRoomSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода броней у комнаты
    """

    class Meta:
        model = Booking
        fields = ("id", "date_start", "date_end")
