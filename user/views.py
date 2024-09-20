import jwt
import stripe
import datetime
from django.shortcuts import redirect
from django.db import IntegrityError
from rest_framework.views import APIView
from middleware.validator import ValidateSchema
from rest_framework.response import Response
from muta_event.settings import (
    COOKIE_ENCRYPTION_SECRET,
    FRONTEND_URL
)
from django.http import JsonResponse
from user.tasks import (
    send_verification_email_task , 
    send_reset_email_task
)
from user.models import User, SubscriptionEnum
from user.schema import (
    UserLoginSchema,
    UserSignupSchema,
    ForgetPasswordSchema,
    ResetPasswordSchema,
    GetVerificationLinkSchema
)
from rest_framework import serializers
from utils.crypto import verify_password, hash_password
from user.google_auth_plugin import GoogleSdkLoginFlowService

class UserLogin(APIView):
    def __init__(self):
        ...

    def get(self,request):
        response = Response()
        token = request.headers.get('Authorization')
        correct_token = False

        if token:
            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
                user = User.objects.get(user_id=payload["user_id"])
                if user:
                    correct_token = True
            except:
                response.data = {"message":"Login failed"}
        
        if not user.is_email_verified:
            response.data = {"message":"Please verify your email"}
            response.status_code = 403
            return response

        if correct_token:
            response.data  = {
                "message":"Login successful.",
                "data":{
                    "user_id":user.user_id,
                    "name":user.first_name + " " + user.last_name,
                    "email":user.email,
                    "subscription_type":user.subscription,
                },
            }
            response.status_code = 200
            return response

        response.data = {"message":"login failed"}
        response.status_code = 500

        return response

    @ValidateSchema(UserLoginSchema)
    def post(self, request):
        response = Response()

        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            response.data = {"message":"Invalid credentials, please try again"}
            response.status_code = 401
            return response

        if not verify_password(
            password=password,
            hashed_password=user.password
        ):
            response.data = {"message":"Invalid credentials, please try again"}
            response.status_code = 401
            return response
        
        if not user.is_email_verified:
            response.data = {"message":"Please verify your email"}
            response.status_code = 403
            return response

        payload = {
            "user_id": str(user.user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*2),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')

        response.set_cookie(key='Authorization', value=token, httponly=True, samesite=None)
        response.data = {
            "message":"Login Succesful",
            "token":token
        }
        return response
    

class UserSignup(APIView):
    def __init__(self):
        ...
    
    @ValidateSchema(UserSignupSchema)
    def post(self, request):
        response = Response()
        user = None
        try:
            user = User.objects.create(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                password= hash_password(request.data['password'])
            )
            user.save()
        except IntegrityError as e:
            response.data = {"message":"User with given credentials already exists"}
            response.status_code = 409
            return response
        except Exception as e:
            response.data = {"message":"Signup failed"}
            response.status_code = 500
            return response
        
        response.data = {
            "message":"Signup successful",
            "data": {
                "user_id": str(user.user_id),
                "name":user.first_name + " " + user.last_name,
                "email":user.email,
                "subscription_type":user.subscription,
            }
        }

        try:
            send_verification_email_task.delay(email=user.email)
        except Exception as e:
            pass

        response.status_code = 200
        return response
    

class ForgetPassword(APIView):
    def __init__(self):
        ...

    @ValidateSchema(ForgetPasswordSchema)
    def post(self, request):
        user = None
        response = Response()
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            print(e)
            response.data = {"message":"Password reset failed"}
            response.status_code = 500
            return response 

        send_reset_email_task.delay(email=email, user_id=user.user_id)
        
        response.data = {"message":"Password reset link sent to your email if email exists"}
        response.status_code = 200
        return response
    
class ResetPassword(APIView):
    def __init__(self):
        ...
    @ValidateSchema(ResetPasswordSchema)
    def post(self, request):
        response = Response()
        token = request.data['token']
        new_password = request.data['new_password']

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
            user = User.objects.get(user_id=payload["user_id"])

            if not user:
                response.data = {"message":"Password reset failed"}
                response.status_code = 500
                return response

            user.password = hash_password(new_password)
            user.save()
        except Exception as e:
            response.data = {"message":"Password reset failed"}
            response.status_code = 500
            return response
        
        response.data = {"message":"Password reset successful"}
        return response
    
class GetVerificationLink(APIView):
    def __init__(self):
        ...

    @ValidateSchema(GetVerificationLinkSchema)
    def post(self, request):
        response = Response()
        email = request.data['email']
        try:
            send_verification_email_task.delay(email,)
        except Exception as e:
            response.data = {"message":"Email verification failed"}
            response.status_code = 500
            return response

        response.data = {"message":"Email verification link sent to your email if email exists"}
        response.status_code = 200
        return response

class VerifyEmail(APIView):
    def __init__(self):
        ...

    def get(self, request):
        response = Response()
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
            user = User.objects.get(email=payload["email"])
            if not user:
                response.data = {"message":"User not found"}
                response.status_code = 404
                return response
            user.is_email_verified = True
            user.save()
        except Exception as e:
            response.data = {"message":"Email verification failed"}
            response.status_code = 500
            return response
        
        response.data = {"message":"Email verified successfully"}
        response.status_code = 200
        return response

class GetUserData(APIView):
    def __init__(self):
        ...
    
    def get(self, request):
        response = Response()
        user = request.muta_user
        response.data = {
            "user_id": str(user.user_id),
            "name":user.first_name + " " + user.last_name,
            "email":user.email,
            "subscription_type":user.subscription,
        }
        response.status_code = 200
        return response
    
class GoogleAuthRedirect(APIView):
    def __init__(self):
        ...
    
    def get(self, request):
        response = Response()
        google_login = GoogleSdkLoginFlowService()

        auth_url, state = google_login.get_authorization_url()

        request.session['google_oauth2_state'] = state

        return redirect(auth_url)


class GoogleAuthCallback(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)


    def __init__(self):
        ...

    def get(self, request, *args, **kwargs):
        response = Response()
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            response.data = {"message": error}
            response.status_code = 400
            return response
        
        if code is None or state is None:
            response.data = {"message": "Invalid request"}
            response.status_code = 400
            return response

        session_state = request.session.get("google_oauth2_state")

        if session_state is None:
            response.data = {"message": "Invalid request"}
            response.status_code = 400
            return response

        del request.session["google_oauth2_state"]

        if state != session_state:
            response.data = {"message": "Invalid request"}
            response.status_code = 400
            return response
        
        google_login_flow = GoogleSdkLoginFlowService()

        google_tokens = google_login_flow.get_tokens(code=code, state=state)

        id_token_decoded = google_login_flow.decode_id_token(id_token=google_tokens.id_token)
        user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        user_email = id_token_decoded["email"]

        muta_user = None

        try:
            muta_user = User.objects.get(email=user_email)
            print(muta_user)
        except User.DoesNotExist:
            muta_user = User.objects.create(
                email=user_email,
                first_name=user_info["given_name"],
                last_name=user_info["family_name"],
                is_email_verified=True,
                subscription=SubscriptionEnum.BASIC.internal,
            )
            muta_user.save()
        except Exception as e:
            response.data = {"message": "Something went wrong"}
            response.status_code = 500
            return response

        payload = {
            "user_id": str(muta_user.user_id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*2),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        response.set_cookie('Authorization', token, httponly=True, samesite=None)

        return redirect(FRONTEND_URL + f'/profile?token={token}')
    
def buy_premium_plan(request):
    if request.method != 'GET':
        return JsonResponse({"message":"Method not allowed"}, status=405)
    
    checkout_session = None
    base_url = request.build_absolute_uri('/')
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1Q0sMNP01A1kBUrCzNPUe8Lr',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= base_url + 'user/get-user-data',
            cancel_url= FRONTEND_URL + '?canceled=true',
        )
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Payment failed"}, status=500)

    if not checkout_session:
        JsonResponse({"message":"Payment failed"}, status=500)
    
    return redirect(checkout_session.url, code=303)