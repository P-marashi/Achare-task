from django.urls import path
from achare.authentication.apis.authentication_api import UserAuthentication


urlpatterns = [
    path("authentication/user/", UserAuthentication.as_view(), name="Status"),
]
