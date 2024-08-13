# messages.py
from django.utils.translation import gettext as _

# Authentication Messages
OTP_SENT = _("otp sent to mobile number.")
INVALID_OR_EXPIRED_NONCE = _("expired nonce.")
INVALID_OR_EXPIRED_OTP = _("Invalid or expired Code.")
INVALID_PASSWORD = _("Invalid password")
PROFILE_UPDATED_SUCCESSFULLY = _("Profile updated successfully.")
ERROR_IN_UPDATE_PROFILE = _("Unexpected error while updating profile")
TOO_MANY_FAILED_ATTEMPTS = _("Too many failed attempts. Try again in {minutes} minutes."
)

# custom message for exceptions
CUSTOM_API_EXCEPTION = _("A server error occurred.")
INTERNAL_SERVER_ERROR = _("Internal server error. Please try again.")
ERROR_DURING_AUTHENTICATE = _("Error during user authentication by mobile")