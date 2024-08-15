import logging
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from achare.utils.helper_functions import (
    is_blocked,
    reset_failed_attempts,
    increment_failed_attempts,
    clean_up_cache,
)
from achare.core.jwt import generate_user_token
from achare.core.messages import (
    INVALID_OR_EXPIRED_NONCE,
    TOO_MANY_FAILED_ATTEMPTS,
    INVALID_OR_EXPIRED_OTP,
    INVALID_PASSWORD,
    USER_DOSE_NOT_EXIST,
)
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


def login_user(nonce: str, password: str, ip_address: str) -> Response:
    """Authenticate a user based on nonce and password/OTP."""
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
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    try:
        user = User.objects.get(mobile_number=mobile_number)
    except User.DoesNotExist:
        increment_failed_attempts(ip_address, mobile_number)
        return Response(
            {"detail": USER_DOSE_NOT_EXIST}, status=status.HTTP_400_BAD_REQUEST
        )
    if user.login_method == User.LoginMethod.OTP:
        if password != str(cache.get(f"otp:{mobile_number}")):
            increment_failed_attempts(ip_address, mobile_number)
            return Response(
                {"detail": INVALID_OR_EXPIRED_OTP}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        if not user.check_password(password):
            increment_failed_attempts(ip_address, mobile_number)
            return Response(
                {"detail": INVALID_PASSWORD}, status=status.HTTP_400_BAD_REQUEST
            )

    reset_failed_attempts(ip_address, mobile_number)
    token = generate_user_token(user)
    clean_up_cache(mobile_number, nonce)
    return Response(
        {
            "refresh": token["refresh"],
            "access": token["access"],
        },
        status=status.HTTP_200_OK,
    )
