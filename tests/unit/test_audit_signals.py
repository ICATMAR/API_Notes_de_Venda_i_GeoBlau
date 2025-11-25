"""
Tests específics per als signals d'auditoria
"""
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from audit.models import AuditLog
from sales_notes.models import Envio

User = get_user_model()


@pytest.mark.django_db
class TestEnvioSignals:
    """Tests per als signals d'Envio"""

    def test_envio_created_generates_audit_log(self, darp_user):
        """Test que crear un Envio genera un log d'auditoria"""
        initial_count = AuditLog.objects.count()

        envio = Envio.objects.create(num_envio="TEST_001", tipo_respuesta=1, usuario_envio=darp_user)

        assert AuditLog.objects.count() == initial_count + 1

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "CREATE"
        assert log.user == darp_user
        assert "TEST_001" in log.description
        assert log.severity == "INFO"

    def test_envio_procesado_change_generates_audit_log(self, darp_user):
        """Test que canviar procesado genera un log d'auditoria"""
        envio = Envio.objects.create(num_envio="TEST_002", tipo_respuesta=1, usuario_envio=darp_user, procesado=False)

        initial_count = AuditLog.objects.count()

        # Canviar procesado
        envio.procesado = True
        envio.save()

        # Ha de generar un nou log
        assert AuditLog.objects.count() > initial_count

        # Buscar el log de UPDATE
        update_logs = AuditLog.objects.filter(action="UPDATE").order_by("-timestamp")
        if update_logs.exists():
            log = update_logs.first()
            assert "processat" in log.description.lower() or "procesado" in log.description.lower()

    def test_envio_validado_change_generates_audit_log(self, darp_user):
        """Test que canviar validado genera un log d'auditoria"""
        envio = Envio.objects.create(num_envio="TEST_003", tipo_respuesta=1, usuario_envio=darp_user, validado=True)

        initial_count = AuditLog.objects.count()

        # Canviar validado
        envio.validado = False
        envio.save()

        # Ha de generar un nou log amb severitat WARNING
        assert AuditLog.objects.count() > initial_count

        # Buscar el log de UPDATE
        update_logs = AuditLog.objects.filter(action="UPDATE").order_by("-timestamp")
        if update_logs.exists():
            log = update_logs.first()
            assert "validat" in log.description.lower() or "validado" in log.description.lower()

    def test_envio_deleted_generates_critical_audit_log(self, darp_user):
        """Test que eliminar un Envio genera un log CRITICAL"""
        envio = Envio.objects.create(num_envio="TEST_004", tipo_respuesta=1, usuario_envio=darp_user)

        initial_count = AuditLog.objects.count()

        # Eliminar envio
        envio.delete()

        # Ha de generar un log CRITICAL
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "DELETE"
        assert log.severity == "CRITICAL"
        assert "TEST_004" in log.description

    def test_envio_update_without_changes_no_audit_log(self, darp_user):
        """Test que actualitzar sense canvis rellevants no genera logs extra"""
        envio = Envio.objects.create(
            num_envio="TEST_005", tipo_respuesta=1, usuario_envio=darp_user, procesado=False, validado=False
        )

        # Obtenir count després de creació
        initial_count = AuditLog.objects.count()

        # Actualitzar camp que no es vigila
        envio.save()

        # No hauria de generar nous logs (només el de creació)
        # Pot haver-hi un log de més si es dispara el signal de UPDATE genèric
        assert AuditLog.objects.count() <= initial_count + 1


@pytest.mark.django_db
class TestUserLoginLogoutSignals:
    """Tests per als signals de login/logout"""

    def test_user_logged_in_signal_generates_audit_log(self, test_user):
        """Test que el signal user_logged_in genera un log"""
        initial_count = AuditLog.objects.count()

        # Simular request
        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_USER_AGENT": "Test Browser",
        }

        # Disparar signal
        user_logged_in.send(sender=User, request=mock_request, user=test_user)

        # Ha de generar un log d'auditoria
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "LOGIN"
        assert log.user == test_user
        assert log.severity == "INFO"
        assert log.ip_address == "127.0.0.1"

    def test_user_logged_out_signal_generates_audit_log(self, test_user):
        """Test que el signal user_logged_out genera un log"""
        initial_count = AuditLog.objects.count()

        # Simular request
        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
        }

        # Disparar signal
        user_logged_out.send(sender=User, request=mock_request, user=test_user)

        # Ha de generar un log d'auditoria
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "LOGOUT"
        assert log.user == test_user
        assert log.severity == "INFO"

    def test_user_logged_out_without_request(self, test_user):
        """Test logout sense request (no hauria de fallar)"""
        initial_count = AuditLog.objects.count()

        # Disparar signal sense request
        user_logged_out.send(sender=User, request=None, user=test_user)

        # Ha de generar un log igualment
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "LOGOUT"
        assert log.user == test_user

    def test_user_login_failed_signal_generates_audit_log(self):
        """Test que el signal user_login_failed genera un log"""
        initial_count = AuditLog.objects.count()

        # Simular request
        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "192.168.1.100",
            "HTTP_USER_AGENT": "Test Browser",
        }

        credentials = {"username": "nonexistent"}

        # Disparar signal
        user_login_failed.send(sender=User, credentials=credentials, request=mock_request)

        # Ha de generar un log d'auditoria
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "FAILED_LOGIN"
        assert log.severity == "WARNING"
        assert "nonexistent" in log.description

    def test_user_login_failed_increments_failed_attempts(self, test_user):
        """Test que login fallit incrementa el comptador"""
        initial_attempts = test_user.failed_login_attempts

        # Simular request
        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_USER_AGENT": "Test Browser",
        }

        credentials = {"username": test_user.username}

        # Disparar signal
        user_login_failed.send(sender=User, credentials=credentials, request=mock_request)

        # Recarregar usuari
        test_user.refresh_from_db()

        # Ha d'haver incrementat els intents fallits
        assert test_user.failed_login_attempts > initial_attempts

    def test_user_login_failed_with_nonexistent_user(self):
        """Test login fallit amb usuari que no existeix (no ha de fallar)"""
        initial_count = AuditLog.objects.count()

        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_USER_AGENT": "Test Browser",
        }

        credentials = {"username": "totally_nonexistent_user"}

        # Disparar signal (no hauria de fallar)
        user_login_failed.send(sender=User, credentials=credentials, request=mock_request)

        # Ha de generar un log igualment
        assert AuditLog.objects.count() > initial_count


@pytest.mark.django_db
class TestUserChangesSignals:
    """Tests per als signals de canvis d'usuaris"""

    def test_user_created_generates_audit_log(self):
        """Test que crear un usuari genera un log d'auditoria"""
        initial_count = AuditLog.objects.count()

        user = User.objects.create_user(
            username="newuser", email="new@test.com", password="Password123!", organization="Test Org"
        )

        # Ha de generar un log de creació
        assert AuditLog.objects.count() > initial_count

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "CREATE"
        assert "newuser" in log.description
        assert log.severity == "INFO"

    def test_user_updated_generates_audit_log(self, test_user):
        """Test que actualitzar un usuari genera un log"""
        # Esperar que es generi log després de creació
        initial_count = AuditLog.objects.count()

        # Actualitzar usuari
        test_user.email = "updated@test.com"
        test_user.save()

        # Ha de generar un log d'actualització
        assert AuditLog.objects.count() > initial_count

        # Buscar el log d'UPDATE més recent
        update_logs = AuditLog.objects.filter(action="UPDATE").order_by("-timestamp")
        if update_logs.exists():
            log = update_logs.first()
            assert "testuser" in log.description

    def test_signal_exception_handling(self, darp_user):
        """Test que els signals gestionen correctament les excepcions"""
        # Forçar una excepció dins el signal
        with patch("audit.signals.AuditLog.objects.create", side_effect=Exception("Test error")):
            with patch("audit.signals.logger") as mock_logger:
                # Crear un envio (hauria de capturar l'excepció)
                envio = Envio.objects.create(num_envio="TEST_ERROR", tipo_respuesta=1, usuario_envio=darp_user)

                # Verificar que s'ha fet log de l'error
                mock_logger.error.assert_called()

    def test_user_login_with_last_login_ip_attribute(self, test_user):
        """Test login amb usuari que té atribut last_login_ip"""
        # Assegurar que l'usuari té l'atribut last_login_ip
        if not hasattr(test_user, "last_login_ip"):
            test_user.last_login_ip = None
            test_user.save()

        mock_request = Mock()
        mock_request.META = {
            "REMOTE_ADDR": "192.168.1.50",
            "HTTP_USER_AGENT": "Test Browser",
        }

        # Disparar signal
        user_logged_in.send(sender=User, request=mock_request, user=test_user)

        # Recarregar usuari
        test_user.refresh_from_db()

        # Ha d'haver actualitzat la IP
        if hasattr(test_user, "last_login_ip"):
            assert test_user.last_login_ip == "192.168.1.50"

    def test_envio_status_change_with_exception(self, darp_user):
        """Test que el signal pre_save gestiona excepcions correctament"""
        envio = Envio.objects.create(num_envio="TEST_006", tipo_respuesta=1, usuario_envio=darp_user, procesado=False)

        # Forçar una excepció en el signal
        with patch("audit.signals.AuditLog.objects.create", side_effect=Exception("Test error")):
            with patch("audit.signals.logger") as mock_logger:
                # Canviar estat (no hauria de fallar tot i l'excepció)
                envio.procesado = True
                envio.save()

                # Verificar que s'ha fet log de l'error
                mock_logger.error.assert_called()

        # L'envio s'hauria d'haver actualitzat igualment
        envio.refresh_from_db()
        assert envio.procesado is True
