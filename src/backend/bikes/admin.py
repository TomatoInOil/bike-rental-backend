from django.contrib import admin

from .models import Bike


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "status", "rental_cost_per_hour")
    list_filter = ("status",)
    search_fields = ("serial_number",)
    ordering = ("serial_number",)
