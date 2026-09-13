from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_otp_email(self,email, otp):
    send_mail(
        subject="This is you`r OTP code",
        message=f"Your OTP code for resetting your password is: {otp}\nThis code will expire in 2 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )