from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView

app_name = "users"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/users/registration/",
        UserCreateAPIView.as_view(),
        name="user-registration",
    ),
    path(
        f"{settings.API_V1_PREFIX}/token/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        f"{settings.API_V1_PREFIX}/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
]
