from rest_framework import serializers

from .models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания комнат.
    Принимает только description и price.
    """

    class Meta:
        model = Room
        fields = ("description", "price")
        read_only_fields = ("id",)


class RoomGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка всех комнат.
    """

    class Meta:
        model = Room
        fields = "__all__"
