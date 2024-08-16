import logging
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from achare.authentication.helper_functions import (
    send_and_cache_otp,
    generate_and_cache_nonce,
    clean_up_cache,
)
from achare.authentication.helper_functions import (
    is_blocked,
    increment_failed_attempts,
    reset_failed_attempts,
)
from achare.core.jwt import generate_user_token
from django.contrib.auth import get_user_model
from achare.core.messages import (
    OTP_SENT,
    INVALID_OR_EXPIRED_OTP,
    INVALID_OR_EXPIRED_NONCE,
    TOO_MANY_FAILED_ATTEMPTS,
)

User = get_user_model()
logger = logging.getLogger(__name__)


def create_user(mobile_number: str) -> User:
    """Create a new user and mark them as active."""
    user = User.objects.create(mobile_number=mobile_number, is_active=True)
    user.save()
    return user


def handle_new_user_authentication(mobile_number: str) -> Response:
    """
    Handle authentication for a new user by generating an OTP and a unique nonce.
    Returns a Response with the nonce and a message indicating OTP was sent.
    """
    send_and_cache_otp(mobile_number)
    nonce = generate_and_cache_nonce(mobile_number)
    return Response(
        {
            "is_new_user": True,
            "nonce": nonce,
            "message": OTP_SENT,
        },
        status=status.HTTP_200_OK,
    )


def verify_and_authenticate_user(nonce: str, otp: str, ip_address: str) -> Response:
    """Verify the provided OTP and authenticate the user."""
    mobile_number = cache.get(f"hash:{nonce}")
    if not mobile_number:
        return Response(
            {"detail": INVALID_OR_EXPIRED_NONCE}, status=status.HTTP_400_BAD_REQUEST
        )

    is_user_blocked, remaining_time = is_blocked(ip_address, mobile_number)
    if is_user_blocked:
        return Response(
            {
                "detail": TOO_MANY_FAILED_ATTEMPTS.format(time=remaining_time),
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    stored_otp = cache.get(f"otp:{mobile_number}")
    if str(stored_otp) != otp:
        increment_failed_attempts(ip_address, mobile_number)
        return Response(
            {"detail": INVALID_OR_EXPIRED_OTP}, status=status.HTTP_400_BAD_REQUEST
        )

    reset_failed_attempts(ip_address, mobile_number)
    user = create_user(mobile_number)
    token = generate_user_token(user)
    clean_up_cache(mobile_number, nonce)

    return Response(
        {
            "refresh": token["refresh"],
            "access": token["access"],
        },
        status=status.HTTP_200_OK,
    )
