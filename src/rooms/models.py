from django.db import models


class Room(models.Model):
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]  # сортировка по умолчанию по id
        indexes = [
            models.Index(fields=["id"]),  # индекс для ускорения запросов по цене
        ]

    def __str__(self):
        return f"Room {self.pk}: {self.description} - ${self.price}"
