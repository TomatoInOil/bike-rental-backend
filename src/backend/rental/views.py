from django.db import transaction
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from bikes.models import Bike, BikeStatus
from rental.models import Rental, RentalStatus
from rental.serializers import ReadOnlyRentalSerializer, RentalSerializer


class RentalCreateAPIView(generics.CreateAPIView):
    """Арендовать велосипед."""

    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            if Rental.objects.filter(
                user=self.request.user, status=RentalStatus.ACTIVE
            ).exists():
                raise ValidationError("У вас уже есть действующая аренда.")

            bike_obj: Bike = serializer.validated_data["bike"]
            if bike_obj.status != BikeStatus.AVAILABLE:
                raise ValidationError("Этот велосипед не доступен для аренды.")
            self.set_bike_rented(bike_obj)

            serializer.save(user=self.request.user)

    @staticmethod
    def set_bike_rented(bike_obj: Bike):
        bike_obj.status = BikeStatus.RENTED
        bike_obj.save()


class RentalUpdateAPIView(generics.GenericAPIView):
    """Завершить аренду."""

    queryset = Rental.objects.select_related("bike").all()
    serializer_class = ReadOnlyRentalSerializer

    def patch(self, request, *args, **kwargs):
        rental = self.get_object()

        bike_obj = rental.bike
        with transaction.atomic():
            self.close_rental(rental, bike_obj.rental_cost_per_hour)
            self.set_bike_available(bike_obj)

        serializer = self.get_serializer(rental)
        return Response(serializer.data)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), user=self.request.user, status=RentalStatus.ACTIVE
        )

    def close_rental(self, rental: Rental, rental_cost_per_hour: float):
        rental.end_time = timezone.now()
        rental.total_cost = self.calculate_total_cost(
            rental.start_time, rental.end_time, rental_cost_per_hour
        )
        rental.status = RentalStatus.ENDED
        rental.save()

    @staticmethod
    def calculate_total_cost(start_time, end_time, rental_cost_per_hour):
        duration = (end_time - start_time).total_seconds()
        total_cost = round(duration / 3600 * rental_cost_per_hour, 2)
        return total_cost

    @staticmethod
    def set_bike_available(bike_obj: Bike):
        bike_obj.status = BikeStatus.AVAILABLE
        bike_obj.save()


class RentalListAPIView(generics.ListAPIView):
    """Просмотреть историю аренд."""

    serializer_class = RentalSerializer

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user).all()
