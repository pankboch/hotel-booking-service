from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Room(models.Model):
    """
    Модель таблицы для комнат
    """

    description = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]  # сортировка по умолчанию по id

    def __str__(self):
        return f"Room {self.pk}: {self.description} - ${self.price}"
