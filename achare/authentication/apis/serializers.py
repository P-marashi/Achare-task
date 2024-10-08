from achare.utils.regexes import phone_number_regex
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)

    def validate_mobile_number(self, value):
        # Use regex to validate the phone number
        if not phone_number_regex(value):
            raise ValidationError(
                _("Phone number must start with '09' and be 11 digits long.")
            )
        return value


class VerifyOTPSerializer(serializers.Serializer):
    nonce = serializers.CharField(max_length=36)
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, value):
        # Ensure the OTP is exactly 6 characters long
        if len(value) != 6:
            raise ValidationError(_("OTP must be exactly 6 digits."))
        return value


class CompleteProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False)
    date_birth = serializers.DateField(required=False)
    password = serializers.CharField(max_length=200, required=False)


class LoginUserSerializer(serializers.Serializer):
    nonce = serializers.CharField(max_length=36)
    password = serializers.CharField(max_length=50)
