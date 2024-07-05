from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from bikes.models import Bike

User = get_user_model()


class RentalStatus(models.IntegerChoices):
    ACTIVE = 1, "Действующая аренда"
    ENDED = 0, "Завершенная аренда"


class Rental(models.Model):
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
        help_text="Итоговая стоимость аренды, выраженная в рублях.",
    )
    status = models.IntegerField(
        verbose_name="Статус",
        choices=RentalStatus.choices,
        default=RentalStatus.ACTIVE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(status=RentalStatus.ACTIVE),
                name="unique_active_rental_for_user",
            ),
        ]
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ("-start_time",)

    def __str__(self):
        return f"Аренда {self.bike} пользователем {self.user}"
