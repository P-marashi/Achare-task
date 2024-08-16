import logging
import random
import uuid
from typing import Any, Tuple, Optional

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FAILED_ATTEMPTS_LIMIT = 3
BLOCK_DURATION = 3600


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
    # Track failed attempts for the mobile number
    mobile_key = f"failed_attempts:mobile:{mobile_number}"
    if cache.get(mobile_key) is None:
        cache.set(mobile_key, 0, BLOCK_DURATION)
    cache.incr(mobile_key)

    # Track unique mobile numbers associated with the IP address
    ip_key = f"failed_attempts:ip:{ip_address}"
    mobile_list_key = f"failed_attempts:ip:{ip_address}:mobiles"

    # Retrieve and update the list of mobile numbers
    mobile_numbers = cache.get(mobile_list_key, [])
    if mobile_number not in mobile_numbers:
        mobile_numbers.append(mobile_number)
        # Set the updated list with the same TTL
        cache.set(mobile_list_key, mobile_numbers, BLOCK_DURATION)

    # Increment attempts counter for the IP and reset TTL
    cache.set(ip_key, cache.get(ip_key, 0) + 1, BLOCK_DURATION)


def is_blocked(ip_address: str, mobile_number: str) -> Tuple[bool, Optional[int]]:
    # Check mobile attempts
    mobile_key = f"failed_attempts:mobile:{mobile_number}"
    mobile_attempts = cache.get(mobile_key, 0)

    if mobile_attempts >= FAILED_ATTEMPTS_LIMIT:
        remaining_time_seconds = get_remaining_block_time(mobile_key)
        return True, remaining_time_seconds

    # Check unique mobiles associated with the IP
    mobile_list_key = f"failed_attempts:ip:{ip_address}:mobiles"
    mobile_numbers = cache.get(mobile_list_key, [])
    unique_mobiles = len(mobile_numbers)

    if unique_mobiles >= FAILED_ATTEMPTS_LIMIT:
        remaining_time_seconds = get_remaining_block_time(mobile_list_key)
        # remaining_time_minutes = remaining_time_seconds // 60
        return True, remaining_time_seconds

    return False, None


def reset_failed_attempts(ip_address: str, mobile_number: str) -> None:
    cache.delete(f"failed_attempts:mobile:{mobile_number}")
    cache.delete(f"failed_attempts:ip:{ip_address}")
    cache.delete(f"failed_attempts:ip:{ip_address}:mobiles")


def get_remaining_block_time(key: str) -> str:
    """
    Get the remaining time before the block expires, in HH:MM:SS format.
    Returns '00:00:00' if the key does not exist or has expired.
    """
    ttl = cache.ttl(key)
    if ttl > 0:
        hours = ttl // 3600
        minutes = (ttl % 3600) // 60
        seconds = ttl % 60

        # Return formatted time as HH:MM:SS
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return "00:00:00"


def send_otp(otp: int, mobile_number: str) -> bool:
    """
    Send an OTP to the given mobile number.
    Replace with actual implementation.
    """
    # Implementation to send OTP goes here
    return True


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
