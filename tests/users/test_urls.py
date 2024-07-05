import pytest
import tests.conftest as conftest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUsersUrls:
    def test_user_registration(self, client):
        url = reverse("users:user-registration")
        data = {
            "username": conftest.TEST_USERNAME,
            "password": conftest.TEST_PASSWORD,
            "email": conftest.TEST_EMAIL,
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_token_obtain_and_refresh(self, client, existing_user):
        token_pair = self._obtain_token_pair(client, existing_user)

        self._refresh_token(client, token_pair)

    def _refresh_token(self, client: APIClient, token_pair: dict) -> None:
        url = reverse("users:token-refresh")
        response = client.post(url, {"refresh": token_pair["refresh"]})
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def _obtain_token_pair(self, client: APIClient, existing_user: User) -> dict:
        url = reverse("users:token-obtain-pair")
        response = client.post(
            url,
            {"username": existing_user.username, "password": conftest.TEST_PASSWORD},
        )
        assert response.status_code == status.HTTP_200_OK
        assert all(key in response.data for key in ["access", "refresh"])
        return response.data
