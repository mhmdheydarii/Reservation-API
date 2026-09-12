from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import ReservationConfigModel, ReservationModel
from .serializers import ReservetionConfigSerializer, ReservationSerializer

# Create your views here.


class ReservationConfigListView(APIView):

    def get(self, request):
        reservations = ReservationConfigModel.objects.all()
        available_reservation_configs = []

        for reservation in reservations:
            if (
                reservation.expired_date > timezone.now()
                and reservation.reserved_by.count() < reservation.max_limit_reserve
            ):
                available_reservation_configs.append(reservation)

        serializer = ReservetionConfigSerializer(
            available_reservation_configs, many=True
        )
        return Response(serializer.data)



class ReservationCreateView(APIView):

    def post(self, request, pk):
        reservation_config = get_object_or_404(ReservationConfigModel, id=pk)

        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reservation_config=reservation_config)

        return Response("data : Rezerved Successfully")
