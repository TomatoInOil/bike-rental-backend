import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

from bikes.models import Bike
from rental.models import Rental

User = get_user_model()


@pytest.mark.django_db
def test_rental_str():
    rental = Rental(
        user=baker.make(User, username="Cool person"),
        bike=baker.make(Bike, serial_number="Cool bike"),
    )
    assert str(rental) == "Аренда Cool bike пользователем Cool person"
