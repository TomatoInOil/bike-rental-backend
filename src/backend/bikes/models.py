from django.db import models


class BikeStatus(models.IntegerChoices):
    AVAILABLE = 1, "Доступен"
    RENTED = 2, "Арендован"
    MAINTENANCE = 3, "На обслуживании"
    LOST = 4, "Утерян"
    SOLD = 5, "Продан"


class Bike(models.Model):
    serial_number = models.CharField(
        verbose_name="Серийный номер", max_length=50, unique=True
    )
    status = models.IntegerField(
        verbose_name="Статус", choices=BikeStatus.choices, default=BikeStatus.AVAILABLE
    )
    rental_cost_per_hour = models.FloatField(
        verbose_name="Стоимость аренды",
        help_text="Стоимость аренды велосипеда за один час (в рублях)",
    )

    class Meta:
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеды"
        ordering = ("serial_number",)

    def __str__(self):
        return self.serial_number
