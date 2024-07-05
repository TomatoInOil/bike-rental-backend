from django.db import transaction
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from bikes.models import Bike
from bikes.services import check_bike_rentability, set_bike_available, set_bike_rented
from rental.models import Rental, RentalStatus
from rental.serializers import ReadOnlyRentalSerializer, RentalSerializer
from rental.services import check_no_active_rental, record_rental_completion


class RentalCreateAPIView(generics.CreateAPIView):
    """Арендовать велосипед."""

    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            check_no_active_rental(user=self.request.user)

            bike_obj: Bike = serializer.validated_data["bike"]
            check_bike_rentability(bike_obj)
            set_bike_rented(bike_obj)

            serializer.save(user=self.request.user)


class RentalUpdateAPIView(generics.GenericAPIView):
    """Завершить аренду."""

    queryset = Rental.objects.select_related("bike").all()
    serializer_class = ReadOnlyRentalSerializer

    def patch(self, request, *args, **kwargs):
        rental = self.get_object()
        bike_obj = rental.bike
        with transaction.atomic():
            record_rental_completion(rental, bike_obj.rental_cost_per_hour)
            set_bike_available(bike_obj)

        serializer = self.get_serializer(rental)
        return Response(serializer.data)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), user=self.request.user, status=RentalStatus.ACTIVE
        )


class RentalListAPIView(generics.ListAPIView):
    """Просмотреть историю аренд."""

    serializer_class = RentalSerializer

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user).all()
