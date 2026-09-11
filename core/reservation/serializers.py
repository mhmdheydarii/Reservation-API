from rest_framework import serializers
from .models import ReservationConfigModel, ReservationModel


class ReservetionConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReservationConfigModel
        fields = ["id" ,"day_of_week", "max_limit_reserve", "expired_date"]


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReservationModel
        fields = ["first_name", "last_name", "phone_number", "subject"]