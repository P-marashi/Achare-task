from achare.core.models import BaseModel
from achare.utils.validators import validate_phone_number
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("User object should have a mobile_number field")

        user = self.model(mobile_number=mobile_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_active", False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(mobile_number, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    class LoginMethod(models.TextChoices):
        OTP = "otp", _("otp")
        PASSWORD = "password", _("password")

    mobile_number = models.CharField(
        max_length=11, unique=True, validators=[validate_phone_number]
    )
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    login_method = models.CharField(
        max_length=50, choices=LoginMethod, default=LoginMethod.OTP
    )

    USERNAME_FIELD = "mobile_number"

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
