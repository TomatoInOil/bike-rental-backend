import pytest
from rest_framework.exceptions import ValidationError

from bikes.models import Bike, BikeStatus
from bikes.services import check_bike_rentability, set_bike_available, set_bike_rented


@pytest.mark.django_db
def test_set_bike_available(rented_bike):
    set_bike_available(rented_bike)
    updated_bike = Bike.objects.get(pk=rented_bike.pk)
    assert updated_bike.status == BikeStatus.AVAILABLE


@pytest.mark.django_db
def test_set_bike_rented(available_bike):
    set_bike_rented(available_bike)
    updated_bike = Bike.objects.get(pk=available_bike.pk)
    assert updated_bike.status == BikeStatus.RENTED


@pytest.mark.django_db
@pytest.mark.parametrize(
    "bike",
    (
        "available_bike",
        "rented_bike",
    ),
)
def test_check_bike_rentability(request, bike):
    bike_obj = request.getfixturevalue(bike)
    try:
        check_bike_rentability(bike_obj)
        assert bike_obj.status == BikeStatus.AVAILABLE, (
            "Велосипед, который не доступен для аренды,"
            " прошёл проверку на доступность аренды."
        )
    except ValidationError:
        assert bike_obj.status != BikeStatus.AVAILABLE, (
            "Велосипед, который доступен для аренды,"
            " не прошёл проверку на доступность аренды."
        )
