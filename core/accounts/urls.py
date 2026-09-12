from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

app_name = "accounts"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/token/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/token/", TokenVerifyView.as_view(), name="verify"),
]