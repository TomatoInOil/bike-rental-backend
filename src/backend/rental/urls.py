from django.conf import settings
from django.urls import path

from rental.views import RentalCreateAPIView, RentalListAPIView, RentalUpdateAPIView

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/rentals/start/",
        RentalCreateAPIView.as_view(),
        name="rentals-start",
    ),
    path(
        f"{settings.API_V1_PREFIX}/rentals/end/",
        RentalUpdateAPIView.as_view(http_method_names=["patch"]),
        name="rentals-end",
    ),
    path(
        f"{settings.API_V1_PREFIX}/rentals/",
        RentalListAPIView.as_view(),
        name="rentals-list",
    ),
]
