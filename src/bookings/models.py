from django.db import models

from rooms.models import Room


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()

    class Meta:
        ordering = ["date_start"]  # сортировка по умолчанию по дате начала бронирования
        indexes = [
            models.Index(fields=["id"]),  # индекс для ускорения запросов по id
        ]

    def __str__(self):
        return f"Booking for room {self.room} from {self.date_start} to {self.date_end}"
