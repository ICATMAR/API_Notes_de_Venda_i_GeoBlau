"""
Serializers for authentication API endpoints.

This module provides serializers for user management and authentication
following Django REST Framework best practices and security guidelines.

Author: ICATMAR Development Team
Date: October 2025
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from .models import APIUser, AuthenticationToken, AuthenticationAuditLog


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Validates password confirmation and applies Django's password
    validation policies.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text=_('Password must meet security requirements')
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text=_('Must match password field')
    )
    
    class Meta:
        model = APIUser
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'organization',
            'password',
            'password_confirm',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'is_active', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, attrs):
        """
        Validate that password and password_confirm match.
        
        Args:
            attrs (dict): Validated attributes
            
        Returns:
            dict: Validated attributes
            
        Raises:
            serializers.ValidationError: If passwords do not match
        """
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password': _('Password fields do not match')
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user instance.
        
        Args:
            validated_data (dict): Validated user data
            
        Returns:
            User: Created user instance
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details (read-only).
    
    Provides comprehensive user information excluding sensitive data.
    """
    
    is_account_locked = serializers.SerializerMethodField()
    
    class Meta:
        model = APIUser
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'organization',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_locked',
            'locked_until',
            'lock_reason',
            'failed_login_attempts',
            'last_failed_login',
            'last_login',
            'last_login_ip',
            'password_changed_at',
            'must_change_password',
            'created_at',
            'updated_at',
            'is_account_locked'
        ]
        read_only_fields = fields
    
    def get_is_account_locked(self, obj):
        """
        Get current account lock status.
        
        Args:
            obj (User): User instance
            
        Returns:
            bool: True if account is currently locked
        """
        return obj.is_account_locked()


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login credentials.
    
    Accepts username and password for authentication.
    """
    
    username = serializers.CharField(
        required=True,
        help_text=_('Username for authentication')
    )
    
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        help_text=_('User password')
    )
    
    def validate(self, attrs):
        """
        Basic validation of required fields.
        
        Args:
            attrs (dict): Input attributes
            
        Returns:
            dict: Validated attributes
            
        Raises:
            serializers.ValidationError: If required fields are missing
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username or not password:
            raise serializers.ValidationError(
                _('Both username and password are required')
            )
        
        return attrs


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializer for authentication token response.
    
    Provides JWT tokens and user information after successful authentication.
    """
    
    access_token = serializers.CharField(
        read_only=True,
        help_text=_('JWT access token for API authentication')
    )
    
    refresh_token = serializers.CharField(
        read_only=True,
        help_text=_('JWT refresh token for obtaining new access tokens')
    )
    
    token_type = serializers.CharField(
        read_only=True,
        default='Bearer',
        help_text=_('Token type (Bearer)')
    )
    
    expires_in = serializers.IntegerField(
        read_only=True,
        help_text=_('Access token expiration time in seconds')
    )
    
    user = UserSerializer(
        read_only=True,
        help_text=_('Authenticated user information')
    )


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer for token refresh request.
    
    Accepts a refresh token to obtain a new access token.
    """
    
    refresh_token = serializers.CharField(
        required=True,
        help_text=_('Valid refresh token')
    )


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change request.
    
    Validates current password and ensures new password meets requirements.
    """
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text=_('Current password')
    )
    
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text=_('New password (must meet security requirements)')
    )
    
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text=_('Confirm new password')
    )
    
    def validate(self, attrs):
        """
        Validate password change request.
        
        Args:
            attrs (dict): Input attributes
            
        Returns:
            dict: Validated attributes
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': _('New password fields do not match')
            })
        
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password': _('New password must be different from current password')
            })
        
        return attrs
    
    def validate_old_password(self, value):
        """
        Verify that the provided current password is correct.
        
        Args:
            value (str): Current password provided by user
            
        Returns:
            str: Validated password
            
        Raises:
            serializers.ValidationError: If password is incorrect
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Current password is incorrect'))
        return value


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout request.
    
    Optionally accepts a refresh token for revocation.
    """
    
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text=_('Refresh token to revoke (optional)')
    )


class AuthenticationTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for authentication token details.
    
    Provides information about JWT tokens including validity status.
    """
    
    user_username = serializers.CharField(
        source='user.username',
        read_only=True,
        help_text=_('Username of token owner')
    )
    
    is_valid_token = serializers.SerializerMethodField(
        help_text=_('Whether the token is currently valid')
    )
    
    class Meta:
        model = AuthenticationToken
        fields = [
            'id',
            'user',
            'user_username',
            'jti',
            'token_type',
            'issued_at',
            'expires_at',
            'is_revoked',
            'revoked_at',
            'revocation_reason',
            'ip_address',
            'is_valid_token'
        ]
        read_only_fields = fields
    
    def get_is_valid_token(self, obj):
        """
        Check if token is currently valid.
        
        Args:
            obj (AuthenticationToken): Token instance
            
        Returns:
            bool: True if token is valid
        """
        return obj.is_valid()


class AuthenticationAuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for authentication audit log entries.
    
    Provides detailed information about authentication events.
    """
    
    user_username = serializers.CharField(
        source='user.username',
        read_only=True,
        help_text=_('Username associated with the event')
    )
    
    event_type_display = serializers.CharField(
        source='get_event_type_display',
        read_only=True,
        help_text=_('Human-readable event type')
    )
    
    severity_display = serializers.CharField(
        source='get_severity_display',
        read_only=True,
        help_text=_('Human-readable severity level')
    )
    
    class Meta:
        model = AuthenticationAuditLog
        fields = [
            'id',
            'user',
            'user_username',
            'event_type',
            'event_type_display',
            'severity',
            'severity_display',
            'ip_address',
            'user_agent',
            'username_attempted',
            'details',
            'timestamp'
        ]
        read_only_fields = fields