import logging
from django.contrib.auth import get_user_model

from achare.core.jwt import generate_user_token
from achare.authentication.auth_blocking import (
    is_blocked,
    redis_cache,
    clean_up_cache,
    increment_failed_attempts,
)
from achare.core.exceptions import (
    UserBlockedException,
    InvalidNonceException,
    InvalidOTPException,
    InvalidPasswordException,
)

User = get_user_model()
logger = logging.getLogger(__name__)


def login_user(nonce: str, password: str, ip_address: str) -> dict:
    """Authenticate a user based on nonce and password/OTP."""
    mobile_number = redis_cache.get(f"hash:{nonce}")
    if not mobile_number:
        raise InvalidNonceException()

    is_user_blocked, remaining_time = is_blocked(ip_address, mobile_number)
    if is_user_blocked:
        raise UserBlockedException(remaining_time=remaining_time)

    try:
        user = User.objects.get(mobile_number=mobile_number)
    except User.DoesNotExist:
        raise InvalidNonceException()

    if user.login_method == User.LoginMethod.OTP:
        if password != str(redis_cache.get(f"otp:{mobile_number}")):
            increment_failed_attempts(ip_address, mobile_number)
            raise InvalidOTPException()
    else:
        if not user.check_password(password):
            increment_failed_attempts(ip_address, mobile_number)
            raise InvalidPasswordException()

    token = generate_user_token(user)
    clean_up_cache(mobile_number, ip_address, nonce)

    return {
        "refresh": token["refresh"],
        "access": token["access"],
    }
