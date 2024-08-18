from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("User info", {"fields": ("email", "password", "first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_verified",
                    "is_staff",
                ),
            },
        ),
    )
    list_display = ("email", "last_name", "is_superuser", "is_staff", "is_verified")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("created",)


admin.site.register(User, CustomUserAdmin)
