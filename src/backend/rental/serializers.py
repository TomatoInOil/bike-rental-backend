from rest_framework import serializers

from rental.models import Rental


class RentalSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Rental
        fields = (
            "user",
            "bike",
            "start_time",
            "end_time",
            "total_cost",
            "status",
        )
        read_only_fields = (
            "user",
            "start_time",
            "end_time",
            "total_cost",
        )


class ReadOnlyRentalSerializer(RentalSerializer):
    class Meta(RentalSerializer.Meta):
        read_only_fields = RentalSerializer.Meta.fields
