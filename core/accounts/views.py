from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
import secrets

from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    PasswordResetSerializer,
    PasswordResetVerifySerializer,
    PasswordResetCompleteSerializer
    )
from .models import User, OtpTokenModel
from .tasks import send_otp_email
# Create your views here.


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Your account created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"data":"Old Password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"data":"Password changed successfully"})


class PasswordResetView(APIView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"data":"If this email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

        request.session["password_reset_user_id"] = user.id
        otp = secrets.randbelow(10**8)
        otp_password = f"{otp:08d}"
        created_date = timezone.now()
        
        OtpTokenModel.objects.filter(user=user, is_verified=False).delete()

        otp_token = OtpTokenModel.objects.create(otp=make_password(otp_password), 
                                                user=user,
                                                expired_date=created_date+timedelta(minutes=2))

        send_otp_email.delay(email=user.email, otp=otp_password)

        return Response({"data":"Code sent to your email"}, status=status.HTTP_200_OK)



class PasswordResetVerifyView(APIView):

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data["otp_code"]

        user_id = request.session.get("password_reset_user_id")

        if not user_id:
            return Response({"data":"Token is expired"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        otp = OtpTokenModel.objects.filter(
            user=user, 
            is_verified=False
            ).first()
        if not otp or not check_password(otp_code,otp.otp):
            return Response({"data":"This Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.expired_date <= timezone.now():
            return Response({"data":"Token Expired"}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_verified = True
        otp.save()
        request.session["password_reset_verified"] = True

        return Response({"data":"Token is Valid"}, status=status.HTTP_200_OK)


class PasswordResetCompleteView(APIView):

    def post(self, request):
        serializer = PasswordResetCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.session.get("password_reset_user_id")
        verified = request.session.get("password_reset_verified")

        if not user_id or not verified:
            return Response({"data":"Password reset session is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        otp = user.otp_tokens.filter(is_verified=True).first()

        if not otp or not otp.is_verified or otp.expired_date <= timezone.now():
            return Response({"data":"Somthing Went wrong!"},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        otp.delete()

        request.session.pop("password_reset_user_id", None)
        request.session.pop("password_reset_verified", None)

        return Response({"data":"Password Change successfully"}, status=status.HTTP_200_OK)
