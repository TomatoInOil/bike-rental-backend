from django.contrib import admin

from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    date_hierarchy = "start_time"
    list_display = ("user", "bike", "start_time", "end_time", "total_cost")
    readonly_fields = ("start_time",)
    search_fields = ("user__username", "bike__serial_number")
    list_filter = ("status",)
