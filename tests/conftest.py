import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from bikes.models import Bike, BikeStatus

TEST_PASSWORD = "Strong password"
TEST_USERNAME = "Cool-person"
TEST_EMAIL = "beautiful-mail@example.com"
User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authorized_client(client):
    user = baker.make(User)
    client.force_authenticate(user, AccessToken.for_user(user))
    return client


@pytest.fixture
def available_bike():
    return baker.make(Bike, status=BikeStatus.AVAILABLE)


@pytest.fixture
def rented_bike():
    return baker.make(Bike, status=BikeStatus.RENTED)


@pytest.fixture
def existing_user():
    return baker.make(User, password=make_password(TEST_PASSWORD))
