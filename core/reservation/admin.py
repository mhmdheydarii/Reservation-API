from django.contrib import admin
from .models import ReservationModel, ReservationConfigModel

# Register your models here.

@admin.register(ReservationModel)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone_number", "status"]
    search_fields = ["last_name"]
    list_filter = ["status"]

@admin.register(ReservationConfigModel)
class ReservationConfigAdmin(admin.ModelAdmin):
    list_display = ["day_of_week", "max_limit_reserve", "expired_date"]
    search_fields = ["day_of_week"]