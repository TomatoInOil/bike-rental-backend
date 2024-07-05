import pytest
from model_bakery import baker

from bikes.models import Bike

TEST_SERIAL_NUMBER = "CCC333"


@pytest.mark.django_db
def test_bike_str():
    bike = baker.make(Bike, serial_number=TEST_SERIAL_NUMBER)
    assert str(bike) == TEST_SERIAL_NUMBER
