from .regexes import phone_number_regex
from django.core.exceptions import ValidationError


# Custom validator using the phone_number_regex function
def validate_phone_number(value):
    if not phone_number_regex(value):
        raise ValidationError("Invalid phone number format. Please ensure it matches the required pattern.")
