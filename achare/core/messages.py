# messages.py
from django.utils.translation import gettext as _

# Authentication Messages
OTP_SENT = _("otp sent to mobile number.")
INVALID_OR_EXPIRED_NONCE = _("Invalid or expired nonce.")
INVALID_OR_EXPIRED_OTP = _("Invalid or expired Code.")
INVALID_PASSWORD_OR_USERNAME = _("Invalid password or username")
PROFILE_UPDATED_SUCCESSFULLY = _("Profile updated successfully.")
ERROR_IN_UPDATE_PROFILE = _("Unexpected error while updating profile")
ISSUE_IN_UPDATE = _("There was an issue updating the profile.")

# custom message for exceptions
CUSTOM_API_EXCEPTION = _("A server error occurred.")
INTERNAL_SERVER_ERROR = _("Internal server error")
ERROR_DURING_AUTHENTICATE = _("Error during user authentication by mobile")
USER_DOSE_NOT_EXIST = _("User with this mobile number does not exist")
VALUE_ERROR = _("There was an issue updating the profile")
TOO_MANY_FAILED_ATTEMPTS = "Too many failed attempts. Try again in"
