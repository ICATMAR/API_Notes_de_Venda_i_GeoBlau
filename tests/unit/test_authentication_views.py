"""
Tests per a les views d'autenticació personalitzades
"""
from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthenticationAuditLog, AuthenticationToken

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistrationView:
    """Tests per al registre d'usuaris"""

    def test_user_registration_success(self, api_client):
        """Test registre exitós d'usuari"""
        url = reverse("authentication:user_registration")
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "NewPassword123!",
            "password_confirm": "NewPassword123!",
            "organization": "Test Organization",
            "cif_organization": "B12345678",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

        # Verificar que es crea log d'auditoria
        audit_log = AuthenticationAuditLog.objects.filter(event_type="ACCOUNT_CREATED").first()
        assert audit_log is not None
        assert audit_log.user.username == "newuser"

    def test_user_registration_password_mismatch(self, api_client):
        """Test registre amb passwords que no coincideixen"""
        url = reverse("authentication:user_registration")
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "NewPassword123!",
            "password_confirm": "DifferentPassword123!",
            "organization": "Test Organization",
            "cif_organization": "B12345678",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(username="newuser").exists()

    def test_user_registration_duplicate_username(self, api_client, test_user):
        """Test registre amb username que ja existeix"""
        url = reverse("authentication:user_registration")
        data = {
            "username": "testuser",  # Ja existeix
            "email": "another@test.com",
            "password": "NewPassword123!",
            "password_confirm": "NewPassword123!",
            "organization": "Test Organization",
            "cif_organization": "B12345678",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginView:
    """Tests per al login personalitzat"""

    def test_login_success(self, api_client, test_user):
        """Test login exitós"""
        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "TestPassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert "user" in response.data
        assert response.data["token_type"] == "Bearer"

        # Verificar que es creen tokens a la base de dades
        assert AuthenticationToken.objects.filter(user=test_user).exists()

        # Verificar que es crea log d'auditoria
        assert AuthenticationAuditLog.objects.filter(user=test_user, event_type="LOGIN_SUCCESS").exists()

    def test_login_invalid_credentials(self, api_client, test_user):
        """Test login amb credencials invàlides"""
        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "WrongPassword"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data

        # Verificar que es crea log de fallida
        assert AuthenticationAuditLog.objects.filter(user=test_user, event_type="LOGIN_FAILED").exists()

    def test_login_user_not_found(self, api_client):
        """Test login amb usuari inexistent"""
        url = reverse("authentication:login")
        data = {"username": "nonexistent", "password": "SomePassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Verificar que es crea log de fallida sense usuari
        assert AuthenticationAuditLog.objects.filter(username_attempted="nonexistent", event_type="LOGIN_FAILED").exists()

    def test_login_account_locked(self, api_client, test_user):
        """Test login amb compte bloquejat"""
        # Bloquejar el compte
        test_user.locked_until = timezone.now() + timedelta(hours=1)
        test_user.lock_reason = "Too many failed attempts"
        test_user.save()

        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "TestPassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "locked" in response.data["error"].lower()

        # Verificar que es crea log de bloqueig
        assert AuthenticationAuditLog.objects.filter(user=test_user, event_type="LOGIN_BLOCKED").exists()

    def test_login_inactive_account(self, api_client, test_user):
        """Test login amb compte inactiu"""
        test_user.is_active = False
        test_user.save()

        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "TestPassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "inactive" in response.data["error"].lower()


@pytest.mark.django_db
class TestLogoutView:
    """Tests per al logout"""

    def test_logout_success(self, authenticated_client, test_user):
        """Test logout exitós"""
        # Primer obtenir refresh token
        refresh = RefreshToken.for_user(test_user)
        refresh_token_str = str(refresh)

        # Crear token a la base de dades
        AuthenticationToken.objects.create(
            jti=str(refresh["jti"]),
            user=test_user,
            token_type="refresh",
            expires_at=timezone.now() + timedelta(days=7),
            ip_address="127.0.0.1",
        )

        url = reverse("authentication:logout")
        data = {"refresh_token": refresh_token_str}

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data

        # Verificar que el token s'ha revocat
        token = AuthenticationToken.objects.get(jti=str(refresh["jti"]))
        assert token.is_revoked is True

        # Verificar que es crea log d'auditoria
        assert AuthenticationAuditLog.objects.filter(user=test_user, event_type="LOGOUT").exists()

    def test_logout_without_refresh_token(self, authenticated_client, test_user):
        """Test logout sense proporcionar refresh token"""
        url = reverse("authentication:logout")
        data = {}

        response = authenticated_client.post(url, data, format="json")

        # Ha de funcionar igualment (logout local)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_with_invalid_token(self, authenticated_client, test_user):
        """Test logout amb token invàlid"""
        url = reverse("authentication:logout")
        data = {"refresh_token": "invalid_token_string"}

        response = authenticated_client.post(url, data, format="json")

        # Ha de retornar 200 OK (logout sempre té èxit)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_unauthenticated(self, api_client):
        """Test logout sense estar autenticat"""
        url = reverse("authentication:logout")
        data = {}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPasswordChangeView:
    """Tests per al canvi de password"""

    def test_password_change_success(self, authenticated_client, test_user):
        """Test canvi de password exitós"""
        url = reverse("authentication:password_change")
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewPassword456!",
            "new_password_confirm": "NewPassword456!",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data

        # Verificar que el password s'ha canviat
        test_user.refresh_from_db()
        assert test_user.check_password("NewPassword456!")

        # Verificar que es crea log d'auditoria
        assert AuthenticationAuditLog.objects.filter(user=test_user, event_type="PASSWORD_CHANGED").exists()

    def test_password_change_wrong_old_password(self, authenticated_client, test_user):
        """Test canvi de password amb old password incorrecte"""
        url = reverse("authentication:password_change")
        data = {
            "old_password": "WrongPassword123!",
            "new_password": "NewPassword456!",
            "new_password_confirm": "NewPassword456!",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_change_new_passwords_mismatch(self, authenticated_client, test_user):
        """Test canvi de password amb new passwords que no coincideixen"""
        url = reverse("authentication:password_change")
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewPassword456!",
            "new_password_confirm": "DifferentPassword456!",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_change_unauthenticated(self, api_client):
        """Test canvi de password sense estar autenticat"""
        url = reverse("authentication:password_change")
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewPassword456!",
            "new_password_confirm": "NewPassword456!",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfileView:
    """Tests per a l'obtenció del perfil d'usuari"""

    def test_get_profile_success(self, authenticated_client, test_user):
        """Test obtenir perfil d'usuari autenticat"""
        url = reverse("authentication:user_profile")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "username" in response.data
        assert response.data["username"] == "testuser"
        assert "email" in response.data
        assert "organization" in response.data

    def test_get_profile_unauthenticated(self, api_client):
        """Test obtenir perfil sense estar autenticat"""
        url = reverse("authentication:user_profile")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuditLogListView:
    """Tests per al llistat de logs d'auditoria"""

    def test_get_audit_logs_success(self, authenticated_client, test_user):
        """Test obtenir logs d'auditoria de l'usuari"""
        # Crear alguns logs d'auditoria
        AuthenticationAuditLog.objects.create(
            event_type="LOGIN_SUCCESS", user=test_user, ip_address="127.0.0.1", severity="INFO"
        )
        AuthenticationAuditLog.objects.create(
            event_type="PASSWORD_CHANGED", user=test_user, ip_address="127.0.0.1", severity="INFO"
        )

        url = reverse("authentication:audit_logs")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 2

    def test_get_audit_logs_only_own_logs(self, authenticated_client, test_user, admin_user):
        """Test que només retorna logs de l'usuari autenticat"""
        # Crear logs per diferents usuaris
        AuthenticationAuditLog.objects.create(
            event_type="LOGIN_SUCCESS", user=test_user, ip_address="127.0.0.1", severity="INFO"
        )
        AuthenticationAuditLog.objects.create(
            event_type="LOGIN_SUCCESS", user=admin_user, ip_address="127.0.0.1", severity="INFO"
        )

        url = reverse("authentication:audit_logs")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Només ha de retornar els logs del test_user
        for log in response.data:
            if "user" in log and log["user"] is not None:
                assert log["user"] == test_user.id

    def test_get_audit_logs_unauthenticated(self, api_client):
        """Test obtenir logs sense estar autenticat"""
        url = reverse("authentication:audit_logs")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_audit_logs_pagination(self, authenticated_client, test_user):
        """Test que els logs estan limitats a 100"""
        # Crear 150 logs
        for i in range(150):
            AuthenticationAuditLog.objects.create(
                event_type="LOGIN_SUCCESS", user=test_user, ip_address="127.0.0.1", severity="INFO"
            )

        url = reverse("authentication:audit_logs")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Només ha de retornar 100 logs
        assert len(response.data) == 100


@pytest.mark.django_db
class TestHelperFunctions:
    """Tests per a les funcions helper de views"""

    def test_get_client_ip_with_x_forwarded_for(self):
        """Test extracció d'IP amb X-Forwarded-For header"""
        from authentication.views import get_client_ip

        mock_request = Mock()
        mock_request.META = {
            "HTTP_X_FORWARDED_FOR": "192.168.1.1, 10.0.0.1",
            "REMOTE_ADDR": "127.0.0.1",
        }

        ip = get_client_ip(mock_request)

        # Ha de retornar la primera IP de X-Forwarded-For
        assert ip == "192.168.1.1"

    def test_get_client_ip_without_x_forwarded_for(self):
        """Test extracció d'IP sense X-Forwarded-For header"""
        from authentication.views import get_client_ip

        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
        }

        ip = get_client_ip(mock_request)

        assert ip == "127.0.0.1"

    def test_get_client_ip_no_ip_available(self):
        """Test extracció d'IP quan no hi ha IP disponible"""
        from authentication.views import get_client_ip

        mock_request = Mock()
        mock_request.META = {}

        ip = get_client_ip(mock_request)

        assert ip == "unknown"

    def test_get_user_agent(self):
        """Test extracció de user agent"""
        from authentication.views import get_user_agent

        mock_request = Mock()
        mock_request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (Test Browser)",
        }

        user_agent = get_user_agent(mock_request)

        assert user_agent == "Mozilla/5.0 (Test Browser)"

    def test_get_user_agent_not_available(self):
        """Test extracció de user agent quan no està disponible"""
        from authentication.views import get_user_agent

        mock_request = Mock()
        mock_request.META = {}

        user_agent = get_user_agent(mock_request)

        assert user_agent == ""
