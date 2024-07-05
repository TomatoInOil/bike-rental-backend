from rest_framework import serializers

from bikes.models import Bike


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = (
            "id",
            "serial_number",
            "rental_cost_per_hour",
        )
