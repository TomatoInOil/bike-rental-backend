import pytest
import tests.conftest as conftest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegistrationView:
    URL = reverse("users:user-registration")

    def test_user_create(self, client):
        data = {
            "username": conftest.TEST_USERNAME,
            "password": conftest.TEST_PASSWORD,
            "email": conftest.TEST_EMAIL,
        }

        response = client.post(self.URL, data)

        assert response.status_code == status.HTTP_201_CREATED
        data.pop("password")
        assert response.data == data

        assert User.objects.count() == 1
        user = User.objects.get()
        assert user.username == conftest.TEST_USERNAME
        assert user.email == conftest.TEST_EMAIL
        assert user.check_password(conftest.TEST_PASSWORD)

    def test_user_create_missing_fields(self, client):
        response = client.post(self.URL, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Обязательное поле." in response.data["password"]
        assert "Обязательное поле." in response.data["username"]
        assert "Обязательное поле." in response.data["email"]
        assert User.objects.count() == 0
