import logging
from typing import Optional, Tuple

from achare.authentication.helper_functions import (
    generate_and_cache_nonce,
    generate_send_and_cache_otp,
)
from achare.core.messages import ERROR_DURING_AUTHENTICATE
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


def authenticate_user_by_mobile(
    mobile_number: str,
) -> Tuple[Optional[User], Optional[str]]:
    """
    Retrieve an active user by mobile number and generate a nonce if the user exists.
    """
    try:
        user = User.objects.get(mobile_number=mobile_number, is_active=True)
        nonce = generate_and_cache_nonce(mobile_number)
        generate_send_and_cache_otp(mobile_number)
        return user, nonce
    except User.DoesNotExist:
        return None, None
    except Exception as e:
        logger.error(f"{ERROR_DURING_AUTHENTICATE}: {e}")
        return None, None
