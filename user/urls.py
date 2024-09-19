from django.urls import path
from user.views import (
    UserLogin,
    UserSignup,
    ForgetPassword,
    ResetPassword
)

user_endpoints = [
    path("sign-in", UserLogin.as_view(), name="Department Login"),
    path("sign-up",UserSignup.as_view(), name="Add student to department"),
    path("forget-password", ForgetPassword.as_view() ,name="Get Due by Id"),
    path("reset-password", ResetPassword.as_view(), name="Get Dues"),
]