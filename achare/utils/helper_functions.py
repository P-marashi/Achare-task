import logging
import random
import uuid
from typing import Any, Tuple, Optional

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FAILED_ATTEMPTS_LIMIT = 3
BLOCK_DURATION = 120  # 1 hour in seconds


def send_otp(otp: int, mobile_number: str) -> bool:
    """
    Send an OTP to the given mobile number.
    Replace with actual implementation.
    """
    # Implementation to send OTP goes here
    return True


def get_remaining_block_time(key: str) -> int:
    """
    Get the remaining time before the block expires, in seconds.
    Returns 0 if the key does not exist or has expired.
    """
    ttl = cache.ttl(key)
    return ttl if ttl > 0 else 0


def send_and_cache_otp(mobile_number: str) -> str:
    """
    Generate, send, and cache an OTP for the given mobile number.
    Returns the generated OTP.
    """
    otp = random.randint(100000, 999999)
    cache_set(f"otp:{mobile_number}", otp, BLOCK_DURATION)
    send_otp(otp, mobile_number)
    logger.debug(f"Generated and sent OTP: {otp}")
    return otp


def generate_and_cache_nonce(mobile_number: str) -> str:
    """
    Generate and cache a nonce for the given mobile number.
    Returns the generated nonce.
    """
    nonce = str(uuid.uuid4())
    cache_set(f"hash:{nonce}", mobile_number, BLOCK_DURATION)
    logger.debug(f"Generated and cached nonce: {nonce}")
    return nonce


def cache_set(key: str, value: Any, timeout: int = settings.CACHE_TTL) -> None:
    """
    Set a value in the cache with an optional timeout.
    """
    cache.set(key, value, timeout)


def clean_up_cache(mobile_number: str, nonce: str) -> None:
    """
    Remove OTP and nonce from the cache after successful verification.
    """
    cache.delete(f"otp:{mobile_number}")
    cache.delete(f"hash:{nonce}")


def get_client_ip(request) -> str:
    """
    Retrieve the client IP address from the request.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def increment_failed_attempts(ip_address: str, mobile_number: str) -> None:
    """
    Increment the count of failed attempts for the given IP and mobile number.
    Initializes the count if it does not exist.
    """
    ip_key = f"failed_attempts:ip:{ip_address}"
    mobile_key = f"failed_attempts:mobile:{mobile_number}"

    if cache.get(ip_key) is None:
        cache.set(ip_key, 0, BLOCK_DURATION)
    if cache.get(mobile_key) is None:
        cache.set(mobile_key, 0, BLOCK_DURATION)

    cache.incr(ip_key)
    cache.incr(mobile_key)


def is_blocked(ip_address: str, mobile_number: str) -> Tuple[bool, Optional[int]]:
    """
    Check if the IP or mobile number is blocked.
    Block the IP if it has three failed attempts across three different mobile numbers.
    """
    ip_key = f"failed_attempts:ip:{ip_address}"
    mobile_key = f"failed_attempts:mobile:{mobile_number}"
    ip_mobile_combo_key = f"failed_attempts:ip_mobile_combo:{ip_address}:{mobile_number}"

    ip_attempts = cache.get(ip_key, 0)
    mobile_attempts = cache.get(mobile_key, 0)
    ip_mobile_attempts = cache.get(ip_mobile_combo_key, 0)

    if ip_attempts >= FAILED_ATTEMPTS_LIMIT:
        remaining_time_seconds = get_remaining_block_time(ip_key)
        remaining_time_minutes = remaining_time_seconds // 60
        return True, remaining_time_minutes

    if mobile_attempts >= FAILED_ATTEMPTS_LIMIT:
        remaining_time_seconds = get_remaining_block_time(mobile_key)
        remaining_time_minutes = remaining_time_seconds // 60
        return True, remaining_time_minutes

    # Block IP if attempts across 3 different mobile numbers exceed the limit
    if ip_mobile_attempts >= FAILED_ATTEMPTS_LIMIT:
        remaining_time_seconds = get_remaining_block_time(ip_mobile_combo_key)
        remaining_time_minutes = remaining_time_seconds // 60
        return True, remaining_time_minutes

    return False, None


def reset_failed_attempts(ip_address: str, mobile_number: str) -> None:
    """
    Reset the count of failed attempts for the given IP and mobile number.
    Also reset the combination of IP and mobile number.
    """
    cache.delete(f"failed_attempts:ip:{ip_address}")
    cache.delete(f"failed_attempts:mobile:{mobile_number}")
    cache.delete(f"failed_attempts:ip_mobile_combo:{ip_address}:{mobile_number}")