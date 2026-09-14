from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView
from . import views

app_name = "accounts"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/token/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/token/", TokenVerifyView.as_view(), name="verify"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/verify/", views.PasswordResetVerifyView.as_view(), name="password-reset-verify"),
    path("password-reset/complete/", views.PasswordResetCompleteView.as_view(), name="password-reset-complete"),
]