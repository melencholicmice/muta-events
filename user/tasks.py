import jwt
import datetime
from celery import shared_task
from django.core.mail import send_mail
from user.models import User

from muta_event.settings import (
    COOKIE_ENCRYPTION_SECRET,
    FRONTEND_URL,
    EMAIL_HOST_USER
)

def send_email_verification_mail(email):
    payload = {
        "email":email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*2),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
    message = f"Click on the link to verify your email: {FRONTEND_URL}/verify-email?token={token}"
    ## for testing only
    # print(f'http://localhost:3000/user/verify-email?token={token}')
    send_mail(
        subject="Muta Events Email Verification",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )

def send_email_password_reset_mail(email, user_id):
    try:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*2),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        message = f"Click on the link to reset your password: {FRONTEND_URL}/reset-password?token={token}"
        send_mail(
            subject="Muta Events password Reset",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
    except Exception as e:
        pass


@shared_task
def send_verification_email_task(subject, message, from_email, recipient_list):
    print("Sending verification email...")
    send_email_verification_mail(subject, message, from_email, recipient_list)

@shared_task
def send_reset_email_task(email,user_id):
    print("Sending reset email...")
    send_email_password_reset_mail(email,user_id)
