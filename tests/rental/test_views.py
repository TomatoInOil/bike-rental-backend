import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings

from bikes.models import BikeStatus
from rental.models import Rental, RentalStatus

User = get_user_model()


@pytest.mark.django_db
class TestRentalCreate:
    def test_rental_start(self, client, existing_user, available_bike):
        url = reverse("rental:rentals-start")
        data = {"bike": available_bike.id}

        client.force_authenticate(user=existing_user)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        rental = Rental.objects.order_by("-pk").first()
        assert rental.user == existing_user
        assert rental.bike == available_bike
        assert rental.status == RentalStatus.ACTIVE

    def test_rental_start_with_active_rental(
        self, client, existing_user, rented_bike, available_bike
    ):
        Rental.objects.create(user=existing_user, bike=rented_bike)

        url = reverse("rental:rentals-start")
        data = {"bike": available_bike.id}
        client.force_authenticate(user=existing_user)
        response = client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data[api_settings.NON_FIELD_ERRORS_KEY]
            == "У вас уже есть действующая аренда."
        )

        assert Rental.objects.filter(user=existing_user).count() == 1

    def test_rental_start_with_unavailable_bike(
        self, client, existing_user, rented_bike
    ):
        url = reverse("rental:rentals-start")
        data = {"bike": rented_bike.id}
        client.force_authenticate(user=existing_user)
        response = client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data[api_settings.NON_FIELD_ERRORS_KEY]
            == "Этот велосипед не доступен для аренды."
        )

        assert Rental.objects.filter(user=existing_user).count() == 0

    def test_rental_start_unauthenticated(self, client, user_with_five_rentals):
        url = reverse("rental:rentals-start")
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRentalUpdate:
    URL = reverse("rental:rentals-end")

    def test_rental_update_authenticated(self, client, user_with_active_rental):
        user, active_rental = user_with_active_rental
        client.force_authenticate(user=user)
        response = client.patch(self.URL)
        assert response.status_code == status.HTTP_200_OK

        active_rental.refresh_from_db()
        assert active_rental.status == RentalStatus.ENDED
        assert active_rental.bike.status == BikeStatus.AVAILABLE

    def test_rental_update_unauthenticated(self, client, user_with_active_rental):
        response = client.patch(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rental_update_not_found(self, authorized_client):
        response = authorized_client.patch(self.URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRentalList:
    URL = reverse("rental:rentals-list")

    def test_rental_list_authenticated(self, client, renter, user_with_five_rentals):
        client.force_authenticate(user=renter)
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5

    def test_rental_list_unauthenticated(self, client, user_with_five_rentals):
        response = client.get(self.URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
