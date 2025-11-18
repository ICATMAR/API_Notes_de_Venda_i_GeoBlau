"""
Views per al sistema d'autenticació TFM
Implementa autenticació JWT amb auditoria completa
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import timedelta
import logging

from .models import APIUser, AuthenticationToken, AuthenticationAuditLog
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    TokenResponseSerializer,
    TokenRefreshSerializer,
    PasswordChangeSerializer,
    LogoutSerializer,
    AuthenticationAuditLogSerializer
)

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Extract client IP address from request.
    
    Args:
        request: Django REST Framework request object
        
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def get_user_agent(request):
    """
    Extract user agent string from request.
    
    Args:
        request: Django REST Framework request object
        
    Returns:
        str: User agent string
    """
    return request.META.get('HTTP_USER_AGENT', '')


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    Allows anonymous users to create new accounts.
    Logs account creation event for audit purposes.
    
    POST /api/auth/register/
    """
    
    queryset = APIUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        """
        Create user and log registration event.
        
        Args:
            serializer: Validated serializer instance
        """
        user = serializer.save()
        
        # Log account creation event
        AuthenticationAuditLog.log_event(
            event_type='ACCOUNT_CREATED',
            user=user,
            ip_address=get_client_ip(self.request),
            user_agent=get_user_agent(self.request),
            severity='INFO',
            details={
                'username': user.username,
                'email': user.email,
                'organization': user.organization
            }
        )
        
        logger.info(f'New user registered: {user.username}')


class LoginView(APIView):
    """
    API endpoint for user authentication.
    
    Authenticates user credentials and issues JWT tokens.
    Implements account locking for brute force protection.
    
    POST /api/auth/login/
    
    Request body:
        {
            "username": "string",
            "password": "string"
        }
    
    Response (200 OK):
        {
            "access_token": "string",
            "refresh_token": "string",
            "token_type": "Bearer",
            "expires_in": integer,
            "user": {...}
        }
    """
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        """
        Handle login request.
        
        Args:
            request: Django REST Framework request object
            
        Returns:
            Response: JWT tokens and user information on success,
                     error message on failure
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        try:
            user = APIUser.objects.get(username=username)
            
            # Check if account is locked
            if user.is_account_locked():
                AuthenticationAuditLog.log_event(
                    event_type='LOGIN_BLOCKED',
                    user=user,
                    username_attempted=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    severity='WARNING',
                    details={
                        'reason': user.lock_reason,
                        'locked_until': user.locked_until.isoformat() if user.locked_until else None
                    }
                )
                
                logger.warning(f'Login blocked for user {username} - account locked')
                
                return Response({
                    'error': _('Account locked'),
                    'detail': user.lock_reason,
                    'locked_until': user.locked_until
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Check if account is active
            if not user.is_active:
                AuthenticationAuditLog.log_event(
                    event_type='LOGIN_FAILED',
                    user=user,
                    username_attempted=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    severity='WARNING',
                    details={'reason': 'Account inactive'}
                )
                
                logger.warning(f'Login failed for user {username} - account inactive')
                
                return Response({
                    'error': _('Account inactive'),
                    'detail': _('Your account is not active. Please contact support.')
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Verify password
            if not user.check_password(password):
                user.record_failed_login()
                
                AuthenticationAuditLog.log_event(
                    event_type='LOGIN_FAILED',
                    user=user,
                    username_attempted=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    severity='WARNING',
                    details={
                        'reason': 'Invalid password',
                        'failed_attempts': user.failed_login_attempts
                    }
                )
                
                logger.warning(
                    f'Failed login attempt for user {username} - '
                    f'attempt {user.failed_login_attempts}'
                )
                
                return Response({
                    'error': _('Invalid credentials'),
                    'detail': _('Username or password is incorrect')
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Successful authentication - generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Get token lifetime from settings
            access_token_lifetime = getattr(
                settings,
                'SIMPLE_JWT',
                {}
            ).get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=30))
            
            expires_at = timezone.now() + access_token_lifetime
            
            # Store tokens in database
            AuthenticationToken.objects.create(
                jti=str(refresh.access_token['jti']),
                user=user,
                token_type='access',
                expires_at=expires_at,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            refresh_lifetime = getattr(
                settings,
                'SIMPLE_JWT',
                {}
            ).get('REFRESH_TOKEN_LIFETIME', timedelta(days=7))
            
            AuthenticationToken.objects.create(
                jti=str(refresh['jti']),
                user=user,
                token_type='refresh',
                expires_at=timezone.now() + refresh_lifetime,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Update last login information
            user.record_successful_login(ip_address=ip_address)
            
            # Log successful authentication
            AuthenticationAuditLog.log_event(
                event_type='LOGIN_SUCCESS',
                user=user,
                ip_address=ip_address,
                user_agent=user_agent,
                severity='INFO'
            )
            
            AuthenticationAuditLog.log_event(
                event_type='TOKEN_ISSUED',
                user=user,
                ip_address=ip_address,
                user_agent=user_agent,
                severity='INFO',
                details={'token_type': 'access+refresh'}
            )
            
            logger.info(f'Successful login for user {username}')
            
            # Prepare response
            response_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': int(access_token_lifetime.total_seconds()),
                'user': UserSerializer(user).data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except APIUser.DoesNotExist:
            # User not found
            AuthenticationAuditLog.log_event(
                event_type='LOGIN_FAILED',
                username_attempted=username,
                ip_address=ip_address,
                user_agent=user_agent,
                severity='WARNING',
                details={'reason': 'User not found'}
            )
            
            logger.warning(f'Login failed - user not found: {username}')
            
            return Response({
                'error': _('Invalid credentials'),
                'detail': _('Username or password is incorrect')
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    
    Revokes authentication tokens and logs logout event.
    
    POST /api/auth/logout/
    
    Request body (optional):
        {
            "refresh_token": "string"
        }
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Handle logout request.
        
        Args:
            request: Django REST Framework request object
            
        Returns:
            Response: Confirmation message
        """
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        refresh_token = serializer.validated_data.get('refresh_token')
        
        # Revoke refresh token if provided
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                jti = str(token['jti'])
                
                # Revoke in database
                tokens_revoked = AuthenticationToken.objects.filter(
                    jti=jti,
                    user=user
                ).update(
                    is_revoked=True,
                    revoked_at=timezone.now(),
                    revocation_reason='User logout'
                )
                
                # Blacklist token if simplejwt blacklist is enabled
                try:
                    token.blacklist()
                except Exception as e:
                    logger.debug(f'Token blacklist not available: {e}')
                
                if tokens_revoked:
                    logger.info(f'Token revoked for user {user.username}')
            
            except Exception as e:
                logger.error(f'Error revoking token: {e}')
        
        # Log logout event
        AuthenticationAuditLog.log_event(
            event_type='LOGOUT',
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            severity='INFO'
        )
        
        logger.info(f'User logged out: {user.username}')
        
        return Response({
            'message': _('Logout successful'),
            'detail': _('Your session has been terminated')
        }, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    """
    API endpoint for password change.
    
    Allows authenticated users to change their password.
    
    POST /api/auth/password/change/
    
    Request body:
        {
            "old_password": "string",
            "new_password": "string",
            "new_password_confirm": "string"
        }
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Handle password change request.
        
        Args:
            request: Django REST Framework request object
            
        Returns:
            Response: Confirmation message
        """
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        new_password = serializer.validated_data['new_password']
        
        # Change password
        user.set_password(new_password)
        user.password_changed_at = timezone.now()
        user.must_change_password = False
        user.save(update_fields=[
            'password',
            'password_changed_at',
            'must_change_password'
        ])
        
        # Log password change event
        AuthenticationAuditLog.log_event(
            event_type='PASSWORD_CHANGED',
            user=user,
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            severity='INFO'
        )
        
        logger.info(f'Password changed for user {user.username}')
        
        return Response({
            'message': _('Password changed successfully'),
            'detail': _('Your password has been updated')
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve authenticated user profile.
    
    GET /api/auth/profile/
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Return the authenticated user.
        
        Returns:
            User: Current authenticated user
        """
        return self.request.user


class AuditLogListView(generics.ListAPIView):
    """
    API endpoint to retrieve authentication audit logs for current user.
    
    Returns the most recent 100 audit log entries.
    
    GET /api/auth/audit-logs/
    """
    
    serializer_class = AuthenticationAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get audit logs for authenticated user.
        
        Returns:
            QuerySet: User's audit log entries
        """
        user = self.request.user
        return AuthenticationAuditLog.objects.filter(
            user=user
        ).order_by('-timestamp')[:100]