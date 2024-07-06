from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("bikes.urls")),
    path("api/", include("rental.urls")),
    path(
        f"api/{settings.API_V1_PREFIX}/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        f"api/{settings.API_V1_PREFIX}/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
