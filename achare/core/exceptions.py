from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException

from .messages import (
    CUSTOM_API_EXCEPTION,
    INVALID_OR_EXPIRED_OTP,
    TOO_MANY_FAILED_ATTEMPTS,
    INVALID_OR_EXPIRED_NONCE,
)


class CustomAPIException(APIException):
    status_code = 400
    default_detail = CUSTOM_API_EXCEPTION


class InvalidNonceException(APIException):
    status_code = 400
    default_detail = INVALID_OR_EXPIRED_NONCE
    default_code = _("invalid_nonce")


class InvalidOTPException(APIException):
    status_code = 400
    default_detail = INVALID_OR_EXPIRED_OTP
    default_code = _("invalid_otp")


class InvalidPasswordException(APIException):
    """Exception raised for invalid password."""

    status_code = 400
    default_detail = _("invalid username or password")
    default_code = _("invalid_password_or_username")


class UserBlockedException(APIException):
    status_code = 403
    default_detail = TOO_MANY_FAILED_ATTEMPTS
    default_code = "user_blocked"

    def __init__(self, remaining_time: str):
        # Format detail message without extra keys
        detail = f"{self.default_detail} {remaining_time}."
        super().__init__(detail=detail)
