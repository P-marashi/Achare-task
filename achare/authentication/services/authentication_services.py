import logging
from typing import Optional, Tuple
from django.contrib.auth import get_user_model
from achare.authentication.helper_functions import (
    send_and_cache_otp,
    generate_and_cache_nonce,
)

from achare.core.messages import ERROR_DURING_AUTHENTICATE
from django.core.cache import cache

User = get_user_model()
logger = logging.getLogger(__name__)


def authenticate_user_by_mobile(
    mobile_number: str,
) -> Tuple[Optional[User], Optional[str]]:
    """Retrieve active user by mobile number and generate nonce if user exists."""
    try:
        user = User.objects.get(mobile_number=mobile_number, is_active=True)
        nonce = generate_and_cache_nonce(mobile_number)
        send_and_cache_otp(mobile_number)
        return user, nonce
    except User.DoesNotExist:
        return None, None
    except Exception as e:
        logger.error(f"{ERROR_DURING_AUTHENTICATE} :{e}")
        return None, None
