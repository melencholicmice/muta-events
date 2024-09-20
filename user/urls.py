from django.urls import path
from user.views import (
    UserLogin,
    UserSignup,
    ForgetPassword,
    ResetPassword,
    VerifyEmail,
    GetVerificationLink,
    GetUserData,
    buy_premium_plan
)

user_endpoints = [
    path("sign-in", UserLogin.as_view(), name="Department Login"),
    path("sign-up",UserSignup.as_view(), name="Add student to department"),
    path("forget-password", ForgetPassword.as_view() ,name="Get Due by Id"),
    path("reset-password", ResetPassword.as_view(), name="Get Dues"),
    path("verify-email", VerifyEmail.as_view(), name="Verify Email"),
    path("send-verification-link", GetVerificationLink.as_view(), name="Get Verification Link"),
    path("buy-premium-subscription", buy_premium_plan, name="Buy Premium Subscription"),
    path("get-user-data", GetUserData.as_view(), name="Get User Data"),
]