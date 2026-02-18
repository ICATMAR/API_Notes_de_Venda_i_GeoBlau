"""
Django admin configuration for authentication models.

This module provides enhanced admin interfaces for user management,
token management, and audit log viewing.

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import APIAccessLog, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced admin interface for User model.

    Provides comprehensive user management with security features
    such as account locking and password management.
    """

    list_display = [
        "username",
        "email",
        "is_active",
        "last_login",
        "date_joined",
    ]

    list_filter = ["is_active", "is_staff", "is_superuser", "date_joined", "last_login"]

    search_fields = ["username", "email", "first_name", "last_name"]

    ordering = ["-date_joined"]

    readonly_fields = [
        "id",
        "date_joined",
        "last_login",
    ]

    fieldsets = (
        (_("Basic Information"), {"fields": ("id", "username", "email", "first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (
            _("Audit Information"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            _("Basic Information"),
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name", "password1", "password2"),
            },
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    actions = []


@admin.register(APIAccessLog)
class APIAccessLogAdmin(admin.ModelAdmin):
    """
    Admin interface for APIAccessLog model.
    """

    list_display = ["timestamp", "method", "path", "status_code", "user", "ip_address", "response_time_ms"]
    list_filter = ["method", "status_code", "timestamp"]
    search_fields = ["user__username", "path", "ip_address", "request_id"]
    readonly_fields = [
        "id",
        "user",
        "ip_address",
        "method",
        "path",
        "query_params",
        "status_code",
        "user_agent",
        "timestamp",
        "response_time_ms",
        "request_id",
        "error_message",
        "request_body_hash",
    ]
    ordering = ["-timestamp"]

    def has_add_permission(self, request):
        return False
