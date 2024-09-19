import jwt
import datetime
from django.db import IntegrityError
from rest_framework.views import APIView
from middleware.validator import ValidateSchema
from rest_framework.response import Response
from muta_event.settings import COOKIE_ENCRYPTION_SECRET
from user.models import User
from user.schema import (
    UserLoginSchema,
    UserSignupSchema,
    ForgetPasswordSchema,
    ResetPasswordSchema
)
from utils.crypto import verify_password, hash_password


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
            print(type(e))
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
        response.status_code = 200
        return response
    

class ForgetPassword(APIView):
    def __init__(self):
        ...

    @ValidateSchema(ForgetPasswordSchema)
    def post(self, request):
        response = Response()
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            payload = {
                "user_id": str(user.user_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*2),
                "iat": datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
            print(token)
            # :TODO: add send email functionality and send token
        except Exception as e:
            pass

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
