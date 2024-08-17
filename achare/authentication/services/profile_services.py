import logging
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from achare.core.messages import ISSUE_IN_UPDATE
from achare.authentication.apis.serializers import CompleteProfileSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


def update_user_profile(user: User, serializer: CompleteProfileSerializer) -> None:
    """Update the user's profile with the provided data."""
    try:
        update_user_fields(user, serializer)
        user.save()
    except Exception as e:
        logger.error(f"Error in updating profile: {e}")
        raise ValidationError({"detail": ISSUE_IN_UPDATE})


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
