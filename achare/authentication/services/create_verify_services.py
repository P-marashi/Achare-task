import logging

from achare.authentication.auth_blocking import (
    clean_up_cache,
    increment_failed_attempts,
    is_blocked,
    redis_cache,
)
from achare.authentication.helper_functions import (
    generate_and_cache_nonce,
    generate_send_and_cache_otp,
)
from achare.core.exceptions import (
    InvalidNonceException,
    InvalidOTPException,
    UserBlockedException,
)
from achare.core.jwt import generate_user_token
from achare.core.messages import OTP_SENT
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


def create_user(mobile_number):
    user = User.objects.filter(mobile_number=mobile_number).first()
    if not user:
        user = User.objects.create(mobile_number=mobile_number, is_active=True)
    return user


def handle_new_user_authentication(mobile_number: str) -> dict:
    """
    Handle authentication for a new user by generating an OTP and a nonce.
    """
    generate_send_and_cache_otp(mobile_number)
    nonce = generate_and_cache_nonce(mobile_number)

    return {
        "its_new_user": True,
        "nonce": nonce,
        "message": OTP_SENT,
    }


def verify_and_authenticate_user(nonce: str, otp: str, ip_address: str) -> dict:
    """
    Verify the provided OTP and authenticate the user if valid.
    """
    mobile_number = redis_cache.get(f"hash:{nonce}")
    if not mobile_number:
        raise InvalidNonceException()

    is_user_blocked, remaining_time = is_blocked(ip_address, mobile_number)
    if is_user_blocked:
        raise UserBlockedException(remaining_time=remaining_time)
    stored_otp = redis_cache.get(f"otp:{mobile_number}")
    if str(stored_otp) != otp:
        increment_failed_attempts(ip_address, mobile_number)
        raise InvalidOTPException()

    user = create_user(mobile_number)
    token = generate_user_token(user)

    # Clean up Redis cache after successful login
    clean_up_cache(ip_address, mobile_number, nonce)

    return {
        "refresh": token["refresh"],
        "access": token["access"],
    }
