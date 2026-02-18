"""
Views per al sistema d'autenticació
Implementa autenticació JWT amb auditoria completa
"""

import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    PasswordChangeSerializer,
    UserRegistrationSerializer,
    UserSerializer,
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
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "unknown")
    return ip


def get_user_agent(request):
    """
    Extract user agent string from request.

    Args:
        request: Django REST Framework request object

    Returns:
        str: User agent string
    """
    return request.META.get("HTTP_USER_AGENT", "")


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Allows anonymous users to create new accounts.
    Logs account creation event for audit purposes.

    POST /api/auth/register/
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Create user and log registration event.

        Args:
            serializer: Validated serializer instance
        """
        user = serializer.save()

        logger.info(f"New user registered: {user.username}")


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

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        ip_address = get_client_ip(request)

        try:
            user = User.objects.get(username=username)

            # Check if account is locked
            if user.is_account_locked():
                logger.warning(f"Login blocked for user {username} - account locked")

                return Response(
                    {"error": _("Account locked"), "detail": user.lock_reason, "locked_until": user.locked_until},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Check if account is active
            if not user.is_active:
                logger.warning(f"Login failed for user {username} - account inactive")

                return Response(
                    {
                        "error": _("Account inactive"),
                        "detail": _("Your account is not active. Please contact support."),
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Verify password
            if not user.check_password(password):
                user.record_failed_login()

                logger.warning(f"Failed login attempt for user {username}")

                return Response(
                    {"error": _("Invalid credentials"), "detail": _("Username or password is incorrect")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Successful authentication - generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Get token lifetime from settings
            access_token_lifetime = getattr(settings, "SIMPLE_JWT", {}).get(
                "ACCESS_TOKEN_LIFETIME", timedelta(minutes=30)
            )

            # Update last login information
            user.record_successful_login(ip_address=ip_address)

            logger.info(f"Successful login for user {username}")

            # Prepare response
            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": int(access_token_lifetime.total_seconds()),
                "user": UserSerializer(user).data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # User not found
            logger.warning(f"Login failed - user not found: {username}")

            return Response(
                {"error": _("Invalid credentials"), "detail": _("Username or password is incorrect")},
                status=status.HTTP_401_UNAUTHORIZED,
            )


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

        refresh_token = serializer.validated_data.get("refresh_token")

        # Revoke refresh token if provided
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                # Blacklist token if simplejwt blacklist is enabled
                token.blacklist()
                logger.info(f"Token blacklisted for user {user.username}")
            except Exception as e:
                logger.debug(f"Error revoking token (blacklist might be disabled): {e}")

        logger.info(f"User logged out: {user.username}")

        return Response(
            {"message": _("Logout successful"), "detail": _("Your session has been terminated")},
            status=status.HTTP_200_OK,
        )


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
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data["new_password"]

        # Change password
        user.set_password(new_password)
        user.password_changed_at = timezone.now()
        user.must_change_password = False
        user.save(update_fields=["password", "password_changed_at", "must_change_password"])

        logger.info(f"Password changed for user {user.username}")

        return Response(
            {"message": _("Password changed successfully"), "detail": _("Your password has been updated")},
            status=status.HTTP_200_OK,
        )


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
