from rest_framework import generics

from bikes.models import Bike, BikeStatus
from bikes.serializers import BikeSerializer


class BikeListAPIView(generics.ListAPIView):
    """Посмотреть список доступных велосипедов."""

    serializer_class = BikeSerializer

    def get_queryset(self):
        return Bike.objects.filter(status=BikeStatus.AVAILABLE).all()
