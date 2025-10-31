"""
Django admin configuration for authentication models.

This module provides enhanced admin interfaces for user management,
token management, and audit log viewing.

"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import APIUser, AuthenticationToken, AuthenticationAuditLog


@admin.register(APIUser)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced admin interface for User model.
    
    Provides comprehensive user management with security features
    such as account locking and password management.
    """
    
    list_display = [
        'username',
        'email',
        'is_active',
        'account_status_badge',
        'failed_login_attempts',
        'last_login',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
        'last_login'
    ]
    
    search_fields = [
        'username',
        'email',
        'full_name',
        'organization'
    ]
    
    ordering = ['-created_at']
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'last_login',
        'last_login_ip',
        'failed_login_attempts',
    ]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'id',
                'username',
                'email',
                'full_name',
                'organization'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Security and Account Locking'), {
            'fields': (
                'is_locked',
                'locked_until',
                'lock_reason',
                'failed_login_attempts',
                'last_failed_login'
            )
        }),
        (_('Password Management'), {
            'fields': (
                'password',
                'password_changed_at',
                'must_change_password',
                'password_history'
            )
        }),
        (_('Audit Information'), {
            'fields': (
                'last_login',
                'last_login_ip',
                'last_login_user_agent',
                'created_at',
                'updated_at',
                'created_by'
            )
        }),
    )
    
    add_fieldsets = (
        (_('Basic Information'), {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'full_name',
                'organization',
                'password1',
                'password2'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )
    
    actions = [
        'unlock_selected_accounts',
        'lock_selected_accounts',
        'reset_failed_attempts'
    ]
    
    def account_status_badge(self, obj):
        """
        Display account status with color-coded badge.
        
        Args:
            obj (User): User instance
            
        Returns:
            str: HTML formatted status badge
        """
        if obj.is_account_locked():
            return format_html(
                '<span style="color: white; background-color: #dc3545; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                'LOCKED</span>'
            )
        elif not obj.is_active:
            return format_html(
                '<span style="color: white; background-color: #fd7e14; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                'INACTIVE</span>'
            )
        else:
            return format_html(
                '<span style="color: white; background-color: #28a745; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                'ACTIVE</span>'
            )
    
    account_status_badge.short_description = _('Status')
    
    def unlock_selected_accounts(self, request, queryset):
        """
        Admin action to unlock selected user accounts.
        
        Args:
            request: HTTP request object
            queryset: Selected user queryset
        """
        count = queryset.update(
            is_locked=False,
            locked_until=None,
            failed_login_attempts=0,
            lock_reason=''
        )
        self.message_user(
            request,
            _(f'{count} account(s) have been unlocked')
        )
    
    unlock_selected_accounts.short_description = _(
        'Unlock selected accounts'
    )
    
    def lock_selected_accounts(self, request, queryset):
        """
        Admin action to lock selected user accounts.
        
        Args:
            request: HTTP request object
            queryset: Selected user queryset
        """
        count = queryset.update(
            is_locked=True,
            locked_until=timezone.now() + timezone.timedelta(hours=24),
            lock_reason=_('Locked manually by administrator')
        )
        self.message_user(
            request,
            _(f'{count} account(s) have been locked')
        )
    
    lock_selected_accounts.short_description = _(
        'Lock selected accounts'
    )
    
    def reset_failed_attempts(self, request, queryset):
        """
        Admin action to reset failed login attempts counter.
        
        Args:
            request: HTTP request object
            queryset: Selected user queryset
        """
        count = queryset.update(
            failed_login_attempts=0,
            last_failed_login=None
        )
        self.message_user(
            request,
            _(f'Failed login attempts reset for {count} account(s)')
        )
    
    reset_failed_attempts.short_description = _(
        'Reset failed login attempts'
    )


@admin.register(AuthenticationToken)
class AuthenticationTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for AuthenticationToken model.
    
    Provides token management and revocation capabilities.
    """
    
    list_display = [
        'jti_display',
        'user',
        'token_type',
        'token_status_badge',
        'issued_at',
        'expires_at',
        'ip_address'
    ]
    
    list_filter = [
        'token_type',
        'is_revoked',
        'issued_at',
        'expires_at'
    ]
    
    search_fields = [
        'jti',
        'user__username',
        'user__email',
        'ip_address'
    ]
    
    readonly_fields = [
        'id',
        'jti',
        'user',
        'token_type',
        'issued_at',
        'expires_at',
        'ip_address',
        'user_agent',
        'is_revoked',
        'revoked_at',
        'revoked_by',
        'revocation_reason'
    ]
    
    ordering = ['-issued_at']
    
    fieldsets = (
        (_('Token Information'), {
            'fields': (
                'id',
                'jti',
                'user',
                'token_type'
            )
        }),
        (_('Lifecycle'), {
            'fields': (
                'issued_at',
                'expires_at'
            )
        }),
        (_('Request Context'), {
            'fields': (
                'ip_address',
                'user_agent'
            )
        }),
        (_('Revocation'), {
            'fields': (
                'is_revoked',
                'revoked_at',
                'revoked_by',
                'revocation_reason'
            )
        }),
    )
    
    actions = ['revoke_selected_tokens']
    
    def jti_display(self, obj):
        """
        Display truncated JTI for readability.
        
        Args:
            obj (AuthenticationToken): Token instance
            
        Returns:
            str: Truncated JTI
        """
        return f"{obj.jti[:16]}..."
    
    jti_display.short_description = _('JWT ID')
    
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
                'REVOKED</span>'
            )
        elif timezone.now() > obj.expires_at:
            return format_html(
                '<span style="color: white; background-color: #fd7e14; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                'EXPIRED</span>'
            )
        else:
            return format_html(
                '<span style="color: white; background-color: #28a745; '
                'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
                'VALID</span>'
            )
    
    token_status_badge.short_description = _('Status')
    
    def revoke_selected_tokens(self, request, queryset):
        """
        Admin action to revoke selected tokens.
        
        Args:
            request: HTTP request object
            queryset: Selected token queryset
        """
        count = queryset.update(
            is_revoked=True,
            revoked_at=timezone.now(),
            revocation_reason=_('Revoked manually by administrator')
        )
        self.message_user(
            request,
            _(f'{count} token(s) have been revoked')
        )
    
    revoke_selected_tokens.short_description = _(
        'Revoke selected tokens'
    )


@admin.register(AuthenticationAuditLog)
class AuthenticationAuditLogAdmin(admin.ModelAdmin):
    """
    Admin interface for AuthenticationAuditLog model.
    
    Provides read-only access to authentication audit logs.
    """
    
    list_display = [
        'timestamp',
        'event_type',
        'user_display',
        'severity_badge',
        'ip_address',
        'username_attempted'
    ]
    
    list_filter = [
        'event_type',
        'severity',
        'timestamp'
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'username_attempted',
        'ip_address',
        'user_agent'
    ]
    
    readonly_fields = [
        'id',
        'user',
        'event_type',
        'severity',
        'ip_address',
        'user_agent',
        'username_attempted',
        'details',
        'timestamp'
    ]
    
    ordering = ['-timestamp']
    
    fieldsets = (
        (_('Event Information'), {
            'fields': (
                'id',
                'event_type',
                'severity',
                'timestamp'
            )
        }),
        (_('User'), {
            'fields': (
                'user',
                'username_attempted'
            )
        }),
        (_('Request Context'), {
            'fields': (
                'ip_address',
                'user_agent'
            )
        }),
        (_('Details'), {
            'fields': (
                'details',
            )
        }),
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
        return obj.username_attempted or _('(unknown)')
    
    user_display.short_description = _('User')
    
    def severity_badge(self, obj):
        """
        Display severity with color-coded badge.
        
        Args:
            obj (AuthenticationAuditLog): Log entry instance
            
        Returns:
            str: HTML formatted severity badge
        """
        color_map = {
            'INFO': '#17a2b8',
            'WARNING': '#fd7e14',
            'ERROR': '#dc3545',
            'CRITICAL': '#6c757d'
        }
        
        color = color_map.get(obj.severity, '#6c757d')
        
        return format_html(
            '<span style="color: white; background-color: {}; '
            'padding: 3px 10px; border-radius: 3px; font-weight: bold;">'
            '{}</span>',
            color,
            obj.get_severity_display()
        )
    
    severity_badge.short_description = _('Severity')
    
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