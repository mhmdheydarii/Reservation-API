from django.urls import path
from . import views

app_name = "reservation"

urlpatterns = [
    path("reservation/list/", views.ReservationView.as_view(), name="reservation-list"),
    path("reserve/<int:pk>/", views.ReservationView.as_view(), name="reserve"),
]