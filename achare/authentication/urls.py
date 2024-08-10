from django.urls import path
from rest_framework.routers import SimpleRouter
from apis.authentication_api import AuthenticationViewSet


router = SimpleRouter()
router.register(r'', AuthenticationViewSet.as_view(), basename="authentication")


urlpatterns = [
    path(r'', router.urls)
]