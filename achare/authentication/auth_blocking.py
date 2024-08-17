from typing import Optional, Tuple

import redis

# Initialize Redis
redis_cache = redis.Redis(charset="utf-8", decode_responses=True)

FAILED_ATTEMPTS_LIMIT = 3
BLOCK_DURATION = 3600


def increment_failed_attempts(ip_address: str, mobile_number: str) -> None:
    """
    Increment failed login attempts for a mobile number and IP address.
    """
    mobile_key = f"failed_attempts:mobile:{mobile_number}"

    # Retrieve the current number of failed attempts
    failed_attempts = redis_cache.get(mobile_key)
    if failed_attempts is None:
        # Initialize failed attempts count if not already set
        redis_cache.set(mobile_key, 1, ex=600)
    else:
        # Increment the failed attempts count
        failed_attempts = int(failed_attempts) + 1
        redis_cache.set(mobile_key, failed_attempts, ex=600)

    # Check if failed attempts exceed the limit and block if necessary
    if failed_attempts == FAILED_ATTEMPTS_LIMIT:
        redis_cache.set(f"blocked:mobile:{mobile_number}", "true", ex=BLOCK_DURATION)

    ip_key = f"failed_attempts:ip:{ip_address}"
    redis_cache.sadd(ip_key, mobile_number)
    unique_mobiles_count = redis_cache.scard(ip_key)

    if unique_mobiles_count >= FAILED_ATTEMPTS_LIMIT:
        redis_cache.set(f"blocked:ip:{ip_address}", "true", ex=BLOCK_DURATION)


def is_blocked(ip_address: str, mobile_number: str) -> Tuple[bool, Optional[int]]:
    """
    Check if the user is blocked based on the mobile number or IP address.
    """
    blocked_mobile_key = f"blocked:mobile:{mobile_number}"
    blocked_ip_key = f"blocked:ip:{ip_address}"

    blocked_mobile = redis_cache.get(blocked_mobile_key)
    if blocked_mobile:
        remaining_time_seconds = get_remaining_block_time(blocked_mobile_key)
        return True, remaining_time_seconds

    blocked_ip = redis_cache.get(blocked_ip_key)
    if blocked_ip:
        remaining_time_seconds = get_remaining_block_time(blocked_ip_key)
        return True, remaining_time_seconds

    return False, None


def get_remaining_block_time(key: str) -> str:
    """
    Get the remaining block time for the given key.
    """
    ttl = redis_cache.ttl(key)
    if ttl > 0:
        hours = ttl // 3600
        minutes = (ttl % 3600) // 60
        seconds = ttl % 60

        # Return formatted time as HH:MM:SS
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return "00:00:00"


def clean_up_cache(ip_address: str, mobile_number: str, nonce: str) -> None:
    """
    Remove the cache after successful verification.
    """
    redis_cache.delete(f"otp:{mobile_number}")
    redis_cache.delete(f"hash:{nonce}")
    redis_cache.delete(f"failed_attempts:ip:{ip_address}")
    redis_cache.delete(f"failed_attempts:ip:{ip_address}:mobiles")
