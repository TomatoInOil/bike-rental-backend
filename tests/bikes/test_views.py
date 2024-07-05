import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from bikes.models import Bike, BikeStatus


@pytest.mark.django_db
class TestBikeList:
    URL = reverse("bikes:bikes-list")

    def test_bike_list(self, authorized_client, three_available_bikes):
        unavailable_bikes = [
            baker.make(Bike, status=BikeStatus.RENTED),
            baker.make(Bike, status=BikeStatus.MAINTENANCE),
            baker.make(Bike, status=BikeStatus.LOST),
            baker.make(Bike, status=BikeStatus.SOLD),
        ]
        response = authorized_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3

        response_bike_ids = [bike["id"] for bike in response.data["results"]]
        for bike in unavailable_bikes:
            assert bike.id not in response_bike_ids

    def test_bike_list_unauthenticated(self, client, three_available_bikes):
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
