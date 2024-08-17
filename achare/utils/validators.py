import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


# Custom validator using the phone_number_regex
def validate_phone_number(value):
    # Pattern: starts with 09 followed by 9 digits
    if not re.match(r"^09\d{9}$", value):
        raise ValidationError(
            _("Invalid phone number format. Please ensure it matches the required pattern.")
        )
