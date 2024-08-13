import logging
from typing import Any

from achare.authentication.services.authentication_services import (
    authenticate_user_by_mobile,
)
from achare.authentication.services.create_verify_services import (
    handle_new_user_authentication,
    verify_and_authenticate_user,
)
from achare.authentication.services.login_services import login_user
from achare.authentication.services.profile_services import update_user_profile
from achare.utils.helper_functions import get_client_ip
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AuthenticationSerializer,
    CompleteProfileSerializer,
    LoginUserSerializer,
    VerifyOTPSerializer,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UserAuthentication(APIView):
    """
    Handle user authentication by
    checking if the user exists and
    sending OTP if needed.
    """

    @extend_schema(tags=["account"], request=AuthenticationSerializer)
    def post(self, request: Any) -> Response:
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_number: str = serializer.validated_data["mobile_number"]
            user, nonce = authenticate_user_by_mobile(mobile_number)

            if user:
                response_data = {
                    "its_new_user": False,
                    "nonce": nonce,
                    "login_method": user.login_method,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            return handle_new_user_authentication(mobile_number)


class VerifyOtp(APIView):
    """Verify the OTP provided by the user to authenticate him."""

    @extend_schema(tags=["account"], request=VerifyOTPSerializer)
    def post(self, request: Any) -> Response:
        ip_address = get_client_ip(request)
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            nonce = serializer.validated_data["nonce"]
            otp = serializer.validated_data["otp"]
            return verify_and_authenticate_user(nonce, otp, ip_address)


class CompleteProfile(APIView):
    """Complete or update the user's profile information."""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["account"], request=CompleteProfileSerializer)
    def put(self, request: Any) -> Response:
        user = request.user
        serializer = CompleteProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return update_user_profile(user, serializer)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    """login user with there password or if they dont have password with otp"""

    @extend_schema(tags=["account"], request=LoginUserSerializer)
    def post(self, request):
        ip_address = get_client_ip(request)
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            nonce = serializer.validated_data["nonce"]
            password = serializer.validated_data["password"]
            return login_user(nonce, password, ip_address)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
