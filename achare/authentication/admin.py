from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "mobile_number",
        "name",
        "last_name",
        "email",
        "login_method",
        "is_admin",
        "is_active",
    )
    list_filter = ("is_admin", "is_active")

    fieldsets = (
        (None, {"fields": ("mobile_number", "password")}),
        (_("Personal info"), {"fields": ("last_name", "email", "date_birth")}),
        (
            _("Permissions"),
            {"fields": ("is_admin", "is_active", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "mobile_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_admin",
                ),
            },
        ),
    )

    search_fields = ("mobile_number", "email", "last_name")
    ordering = ("mobile_number",)


admin.site.register(User, UserAdmin)
