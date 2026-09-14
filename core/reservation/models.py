from django.db import models
from accounts.models import User
from django.utils import timezone
from accounts.validators import validate_iranian_cellphone_number
# Create your models here.


class ReservationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15 ,validators=[validate_iranian_cellphone_number])
    subject = models.CharField(max_length=1000)
    reservation_config = models.ForeignKey("ReservationConfigModel", on_delete=models.CASCADE)
    class ReservationStatusModel(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(default=ReservationStatusModel.PENDING, choices=ReservationStatusModel.choices, max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ReservationConfigModel(models.Model):
    day_of_week = models.CharField(max_length=100, null=True, blank=True)
    max_limit_reserve = models.PositiveIntegerField(default=0)
    expired_date = models.DateTimeField(default=timezone.now)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.day_of_week

    class Meta:
        ordering = ["-created_date"]