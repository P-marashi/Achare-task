import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    """Test creating a user instance using the User model manager."""
    user = User.objects.create_user(mobile_number="09100953795", password="password123")
    assert user is not None
    assert user.mobile_number == "09100953795"
    assert user.check_password("password123")
    assert user.is_active is False  # Default to inactive


@pytest.mark.django_db
def test_superuser_creation():
    """Test creating a superuser instance using the User model manager."""
    superuser = User.objects.create_superuser(
        mobile_number="09100953796", password="superpassword"
    )
    assert superuser is not None
    assert superuser.mobile_number == "09100953796"
    assert superuser.check_password("superpassword")
    assert superuser.is_active is True
    assert superuser.is_admin is True
