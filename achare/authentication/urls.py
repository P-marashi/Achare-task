from django.urls import path
from achare.authentication.apis.authentication_api import (
    VerifyOtp,
    CompleteProfile,
    UserAuthentication,
    LoginUser)


urlpatterns = [
    path("authentication/user/account", UserAuthentication.as_view(), name="Status"),
    path("authentication/user/verify/", VerifyOtp.as_view(), name="VerifyOtp"),
    path("authentication/user/profile/", CompleteProfile.as_view(), name="profile"),
    path("authentication/user/login/", LoginUser.as_view(), name="login"),
]
