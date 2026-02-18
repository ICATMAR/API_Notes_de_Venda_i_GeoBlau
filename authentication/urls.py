"""
URLs per al sistema d'autenticació TFM
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import LoginView, LogoutView, PasswordChangeView, UserProfileView, UserRegistrationView

app_name = "authentication"

urlpatterns = [
    # User registration and profile management
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    # Authentication endpoints
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # JWT token management
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Password management
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
]
