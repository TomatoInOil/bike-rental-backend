from rest_framework import generics

from bikes.models import Bike
from bikes.serializers import BikeSerializer


class BikeListAPIView(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        return Bike.objects.filter(status=Bike.Status.AVAILABLE).all()
