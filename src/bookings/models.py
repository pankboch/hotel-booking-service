from django.db import models

from rooms.models import Room


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()

    class Meta:
        ordering = ("date_start",)  # сортировка по дате начала бронирования

    def __str__(self):
        return f"Booking for room {self.room} from {self.date_start} to {self.date_end}"
