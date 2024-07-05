from datetime import datetime, timezone

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

from bikes.models import Bike, BikeStatus
from rental.models import Rental, RentalStatus

User = get_user_model()


@pytest.fixture
def renter():
    user = baker.make(User)
    return user


@pytest.fixture
def user_with_five_rentals(renter):
    baker.make(Rental, user=renter, status=RentalStatus.ACTIVE)
    baker.make(Rental, user=renter, status=RentalStatus.ENDED, _quantity=4)


@pytest.fixture
def user_with_active_rental(mocker):
    mocker.patch(
        "django.utils.timezone.now",
        return_value=datetime(2024, 7, 5, 0, 0, 0, tzinfo=timezone.utc),
    )
    user = baker.make(User)
    bike = baker.make(Bike, status=BikeStatus.RENTED)
    rental = baker.make(Rental, user=user, bike=bike, status=RentalStatus.ACTIVE)
    return user, rental


@pytest.fixture
def user_with_ended_rental(mocker):
    mocker.patch(
        "django.utils.timezone.now",
        return_value=datetime(2024, 7, 5, 0, 0, 0, tzinfo=timezone.utc),
    )
    user = baker.make(User)
    bike = baker.make(Bike, status=BikeStatus.AVAILABLE)
    rental = baker.make(Rental, user=user, bike=bike, status=RentalStatus.ENDED)
    return user, rental
