from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from bikes.models import Bike, BikeStatus


def set_bike_available(bike_obj: Bike) -> None:
    """Изменяет статус велосипеда на `Доступен`, сохраняет объект."""
    bike_obj.status = BikeStatus.AVAILABLE
    bike_obj.save()


def set_bike_rented(bike_obj: Bike) -> None:
    """Изменяет статус велосипеда на `Арендован`, сохраняет объект."""
    bike_obj.status = BikeStatus.RENTED
    bike_obj.save()


def check_bike_rentability(bike_obj: Bike) -> None:
    """Вызывает исключение ValidationError, если велосипед не доступен для аренды."""
    if bike_obj.status != BikeStatus.AVAILABLE:
        raise ValidationError(
            {
                api_settings.NON_FIELD_ERRORS_KEY: (
                    "Этот велосипед не доступен для аренды."
                )
            }
        )
