from datetime import datetime, timezone

import pytest
from django.contrib.auth import get_user_model

from rental.models import Rental, RentalStatus

User = get_user_model()


@pytest.fixture
def user_with_active_rental(mocker, rented_bike):
    mocker.patch(
        "django.utils.timezone.now",
        return_value=datetime(2024, 7, 5, 0, 0, 0, tzinfo=timezone.utc),
    )
    user = User.objects.create(username="user_with_active_rental")
    rental = Rental.objects.create(user=user, bike=rented_bike)
    return user, rental


@pytest.fixture
def user_with_ended_rental(mocker, available_bike):
    mocker.patch(
        "django.utils.timezone.now",
        return_value=datetime(2024, 7, 5, 0, 0, 0, tzinfo=timezone.utc),
    )
    user = User.objects.create(username="user_with_ended_rental")
    rental = Rental.objects.create(
        user=user, bike=available_bike, status=RentalStatus.ENDED
    )
    return user, rental
