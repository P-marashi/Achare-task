import logging
from rest_framework.response import Response
from rest_framework import status
from achare.core.messages import (
    PROFILE_UPDATED_SUCCESSFULLY,
    INTERNAL_SERVER_ERROR,
    ERROR_IN_UPDATE_PROFILE,
)
from achare.authentication.apis.serializers import CompleteProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


def update_user_profile(user: User, serializer: CompleteProfileSerializer) -> Response:
    """Update the user's profile with the provided data."""
    try:
        update_user_fields(user, serializer)
        user.save()
        return Response(
            {"detail": PROFILE_UPDATED_SUCCESSFULLY}, status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"{ERROR_IN_UPDATE_PROFILE}: {e}")
        return Response(
            {"detail": INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def update_user_fields(user: User, serializer: CompleteProfileSerializer) -> None:
    """Update the fields of the user object."""
    user.name = serializer.validated_data.get("name", user.name)
    user.last_name = serializer.validated_data.get("last_name", user.last_name)
    user.email = serializer.validated_data.get("email", user.email)
    user.date_birth = serializer.validated_data.get("date_birth", user.date_birth)
    password = serializer.validated_data.get("password", None)
    if password:
        user.set_password(password)
        user.login_method = User.LoginMethod.PASSWORD
