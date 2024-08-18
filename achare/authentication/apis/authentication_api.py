import logging
from typing import Any

from achare.authentication.auth_blocking import is_blocked
from achare.authentication.helper_functions import get_client_ip
from achare.authentication.services.authentication_services import (
    authenticate_user_by_mobile,
)
from achare.authentication.services.create_verify_services import (
    handle_new_user_authentication,
    verify_and_authenticate_user,
)
from achare.authentication.services.login_services import login_user
from achare.authentication.services.profile_services import update_user_profile
from achare.core.exceptions import (
    InvalidNonceException,
    InvalidOTPException,
    InvalidPasswordException,
    UserBlockedException,
)
from achare.core.messages import (
    INTERNAL_SERVER_ERROR,
    INVALID_OR_EXPIRED_NONCE,
    INVALID_OR_EXPIRED_OTP,
    INVALID_PASSWORD_OR_USERNAME,
    PROFILE_UPDATED_SUCCESSFULLY,
)
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    Handle user authentication by checking if the user exists
    and sending an OTP if needed.
    """

    @extend_schema(tags=["account"], request=AuthenticationSerializer)
    def post(self, request: Any) -> Response:
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = get_client_ip(request)
        mobile_number: str = serializer.validated_data["mobile_number"]
        is_user_blocked, remaining_time = is_blocked(ip_address, mobile_number)
        if is_user_blocked:
            raise UserBlockedException(remaining_time=remaining_time)
        user, nonce = authenticate_user_by_mobile(mobile_number)

        if user:
            response_data = {
                "its_new_user": False,
                "nonce": nonce,
                "login_method": user.login_method,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        new_user_data = handle_new_user_authentication(mobile_number)
        return Response(new_user_data, status=status.HTTP_200_OK)


class VerifyOtp(APIView):
    """Verify the OTP provided by the user to authenticate them."""

    @extend_schema(tags=["account"], request=VerifyOTPSerializer)
    def post(self, request: Any) -> Response:
        ip_address = get_client_ip(request)
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nonce = serializer.validated_data["nonce"]
        otp = serializer.validated_data["otp"]

        try:
            tokens = verify_and_authenticate_user(nonce, otp, ip_address)
            return Response(tokens, status=status.HTTP_201_CREATED)
        except UserBlockedException as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except InvalidNonceException:
            return Response(
                {"detail": INVALID_OR_EXPIRED_NONCE}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidOTPException:
            return Response(
                {"detail": INVALID_OR_EXPIRED_OTP}, status=status.HTTP_400_BAD_REQUEST
            )


class CompleteProfile(APIView):
    """Complete or update the user's profile information."""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["account"], request=CompleteProfileSerializer)
    def put(self, request: Any) -> Response:
        user = request.user
        serializer = CompleteProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            update_user_profile(user, serializer)
            return Response(
                {"detail": PROFILE_UPDATED_SUCCESSFULLY}, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in profile update: {e}")
            return Response(
                {"detail": f"{INTERNAL_SERVER_ERROR}: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginUser(APIView):
    """Log in user with their password or OTP."""

    @extend_schema(tags=["account"], request=LoginUserSerializer)
    def post(self, request: Any) -> Response:
        ip_address = get_client_ip(request)
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nonce = serializer.validated_data["nonce"]
        password = serializer.validated_data["password"]

        try:
            tokens = login_user(nonce, password, ip_address)
            return Response(tokens, status=status.HTTP_200_OK)
        except InvalidNonceException:
            return Response(
                {"detail": INVALID_OR_EXPIRED_NONCE}, status=status.HTTP_400_BAD_REQUEST
            )
        except UserBlockedException as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except InvalidOTPException:
            return Response(
                {"detail": INVALID_OR_EXPIRED_OTP}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidPasswordException:
            return Response(
                {"detail": INVALID_PASSWORD_OR_USERNAME},
                status=status.HTTP_400_BAD_REQUEST,
            )
