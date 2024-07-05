from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from rental.models import Rental, RentalStatus

User = get_user_model()


def record_rental_completion(rental: Rental, rental_cost_per_hour: float) -> None:
    """
    Фиксирует время окончания аренды, стоимость и завершенный статус, сохраняет объект.
    """
    rental.end_time = timezone.now()
    rental.total_cost = calculate_total_cost(
        rental.start_time, rental.end_time, rental_cost_per_hour
    )
    rental.status = RentalStatus.ENDED
    rental.save()


def calculate_total_cost(
    start_time: datetime, end_time: datetime, rental_cost_per_hour: float
) -> float:
    """Вычисляет итоговую стоимость аренды."""
    if start_time > end_time:
        raise ValueError("Начальное время не может быть позже конечного времени")
    duration = (end_time - start_time).total_seconds()
    total_cost = round(duration / 3600 * rental_cost_per_hour, 2)
    return total_cost


def check_no_active_rental(user: User) -> None:
    """
    Вызывает исключение ValidationError, если у пользователя уже есть активная аренда.
    """
    if Rental.objects.filter(user=user, status=RentalStatus.ACTIVE).exists():
        raise ValidationError(
            {api_settings.NON_FIELD_ERRORS_KEY: "У вас уже есть действующая аренда."}
        )
