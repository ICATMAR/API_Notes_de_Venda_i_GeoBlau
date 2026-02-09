"""
Django admin configuration for authentication models.

This module provides enhanced admin interfaces for user management,
token management, and audit log viewing.

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import APIAccessLog, AuthenticationAuditLog, AuthenticationToken, User


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


@admin.register(AuthenticationToken)
class AuthenticationTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for AuthenticationToken model.

    Provides token management and revocation capabilities.
    """

    list_display = ["jti_display", "user", "token_type", "token_status_badge", "issued_at", "expires_at", "ip_address"]

    list_filter = ["token_type", "is_revoked", "issued_at", "expires_at"]

    search_fields = ["jti", "user__username", "user__email", "ip_address"]

    readonly_fields = [
        "id",
        "jti",
        "user",
        "token_type",
        "issued_at",
        "expires_at",
        "ip_address",
        "user_agent",
        "is_revoked",
        "revoked_at",
        "revoked_by",
        "revocation_reason",
    ]

    ordering = ["-issued_at"]

    fieldsets = (
        (_("Token Information"), {"fields": ("id", "jti", "user", "token_type")}),
        (_("Lifecycle"), {"fields": ("issued_at", "expires_at")}),
        (_("Request Context"), {"fields": ("ip_address", "user_agent")}),
        (_("Revocation"), {"fields": ("is_revoked", "revoked_at", "revoked_by", "revocation_reason")}),
    )

    actions = ["revoke_selected_tokens"]

    def jti_display(self, obj):
        """
        Display truncated JTI for readability.

        Args:
            obj (AuthenticationToken): Token instance

        Returns:
            str: Truncated JTI
        """
        return f"{obj.jti[:16]}..."

    jti_display.short_description = _("JWT ID")

    def token_status_badge(self, obj):
        """
        Display token status with color-coded badge.

        Args:
            obj (AuthenticationToken): Token instance

        Returns:
            str: HTML formatted status badge
        """
        if obj.is_revoked:
            return format_html(
                '<span style="color: white; background-color: #dc3545; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                "REVOKED</span>"
            )
        elif timezone.now() > obj.expires_at:
            return format_html(
                '<span style="color: white; background-color: #fd7e14; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                "EXPIRED</span>"
            )
        else:
            return format_html(
                '<span style="color: white; background-color: #28a745; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                "VALID</span>"
            )

    token_status_badge.short_description = _("Status")

    def revoke_selected_tokens(self, request, queryset):
        """
        Admin action to revoke selected tokens.

        Args:
            request: HTTP request object
            queryset: Selected token queryset
        """
        count = queryset.update(
            is_revoked=True, revoked_at=timezone.now(), revocation_reason=_("Revoked manually by administrator")
        )
        self.message_user(request, _(f"{count} token(s) have been revoked"))

    revoke_selected_tokens.short_description = _("Revoke selected tokens")


@admin.register(AuthenticationAuditLog)
class AuthenticationAuditLogAdmin(admin.ModelAdmin):
    """
    Admin interface for AuthenticationAuditLog model.

    Provides read-only access to authentication audit logs.
    """

    list_display = ["timestamp", "event_type", "user_display", "severity_badge", "ip_address", "username_attempted"]

    list_filter = ["event_type", "severity", "timestamp"]

    search_fields = ["user__username", "user__email", "username_attempted", "ip_address", "user_agent"]

    readonly_fields = [
        "id",
        "user",
        "event_type",
        "severity",
        "ip_address",
        "user_agent",
        "username_attempted",
        "details",
        "timestamp",
    ]

    ordering = ["-timestamp"]

    fieldsets = (
        (_("Event Information"), {"fields": ("id", "event_type", "severity", "timestamp")}),
        (_("User"), {"fields": ("user", "username_attempted")}),
        (_("Request Context"), {"fields": ("ip_address", "user_agent")}),
        (_("Details"), {"fields": ("details",)}),
    )

    def user_display(self, obj):
        """
        Display user or attempted username.

        Args:
            obj (AuthenticationAuditLog): Log entry instance

        Returns:
            str: Username or attempted username
        """
        if obj.user:
            return obj.user.username
        return obj.username_attempted or _("(unknown)")

    user_display.short_description = _("User")

    def severity_badge(self, obj):
        """
        Display severity with color-coded badge.

        Args:
            obj (AuthenticationAuditLog): Log entry instance

        Returns:
            str: HTML formatted severity badge
        """
        color_map = {"INFO": "#17a2b8", "WARNING": "#fd7e14", "ERROR": "#dc3545", "CRITICAL": "#6c757d"}

        color = color_map.get(obj.severity, "#6c757d")

        return format_html(
            '<span style="color: white; background-color: {}; '
            'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
            "{}</span>",
            color,
            obj.get_severity_display(),
        )

    severity_badge.short_description = _("Severity")

    def has_add_permission(self, request):
        """
        Prevent manual creation of audit logs.

        Returns:
            bool: False (no add permission)
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of audit logs for compliance.

        Returns:
            bool: False (no delete permission)
        """
        return False


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
