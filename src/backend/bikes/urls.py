from django.conf import settings
from django.urls import path

from bikes.views import BikeListAPIView

app_name = "bikes"

urlpatterns = [
    path(
        f"{settings.API_V1_PREFIX}/bikes/",
        BikeListAPIView.as_view(),
        name="bikes-list",
    ),
]
