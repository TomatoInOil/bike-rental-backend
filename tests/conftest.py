import pytest

from bikes.models import Bike, BikeStatus


@pytest.fixture
def rented_bike():
    return Bike.objects.create(
        serial_number="AA123",
        status=BikeStatus.RENTED,
        rental_cost_per_hour=100,
    )


@pytest.fixture
def available_bike():
    return Bike.objects.create(
        serial_number="BB231",
        status=BikeStatus.AVAILABLE,
        rental_cost_per_hour=100,
    )
