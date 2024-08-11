import re
from rest_framework import serializers
from achare.utils.validators import validate_phone_number
from django.core.exceptions import ValidationError


class AuthenticationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    
    def validate_mobile_number(self, value):
        if not value.startswith("09"):
            raise ValidationError("Phone number must start with '09'.")
        if len(value) != 11:
            raise ValidationError("Phone number must be exactly 11 digits.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    unique_hash = serializers.CharField(max_length=36)
    otp = serializers.CharField()
