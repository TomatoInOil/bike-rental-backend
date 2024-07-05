import pytest
from model_bakery import baker

from bikes.models import Bike, BikeStatus


@pytest.fixture
def three_available_bikes():
    return baker.make(Bike, status=BikeStatus.AVAILABLE, _quantity=3)
