from django.contrib.auth import get_user_model
from django.db import models

from bikes.models import Bike

User = get_user_model()


class Rental(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Активная поездка"
        ENDED = 0, "Завершенная поездка"

    user = models.ForeignKey(
        verbose_name="Арендатор",
        to=User,
        on_delete=models.CASCADE,
        related_name="rentals",
    )
    bike = models.ForeignKey(
        verbose_name="Велосипед",
        to=Bike,
        on_delete=models.SET_NULL,
        null=True,
        related_name="rentals",
    )
    start_time = models.DateTimeField(
        verbose_name="Время начала",
        auto_now_add=True,
    )
    end_time = models.DateTimeField(
        verbose_name="Время окончания",
        null=True,
        blank=True,
    )
    total_cost = models.FloatField(
        verbose_name="Итоговая стоимость",
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        verbose_name="Статус поездки",
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"

    def __str__(self):
        return f"Аренда {self.bike} пользователем {self.user}"
