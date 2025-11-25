"""
Tests unitaris per al sistema d'auditoria
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from audit.models import AuditLog, SecurityEvent


@pytest.mark.django_db
class TestAuditLog:
    """Tests per al model AuditLog"""

    def test_audit_log_creation(self, api_user):
        """Test creació bàsica d'un log d'auditoria"""
        log = AuditLog.objects.create(action="CREATE", user=api_user, description="Test audit log", severity="INFO")

        assert log.action == "CREATE"
        assert log.user == api_user
        assert log.severity == "INFO"
        assert log.timestamp is not None

    def test_audit_log_with_old_new_values(self, api_user):
        """Test log amb valors anteriors i nous"""
        log = AuditLog.objects.create(
            action="UPDATE",
            user=api_user,
            description="Actualització envio",
            old_value={"procesado": False},
            new_value={"procesado": True},
            severity="INFO",
        )

        assert log.old_value == {"procesado": False}
        assert log.new_value == {"procesado": True}

    def test_audit_log_without_user(self):
        """Test log sense usuari (operacions automàtiques)"""
        log = AuditLog.objects.create(
            action="SECURITY_EVENT",
            description="Intent de login fallit",
            ip_address="192.168.1.100",
            severity="WARNING",
        )

        assert log.user is None
        assert log.ip_address == "192.168.1.100"

    def test_audit_log_ordering(self, api_user):
        """Test que els logs s'ordenen per timestamp descendent"""
        log1 = AuditLog.objects.create(action="CREATE", user=api_user, description="Primer", severity="INFO")

        log2 = AuditLog.objects.create(action="CREATE", user=api_user, description="Segon", severity="INFO")

        logs = list(AuditLog.objects.all())
        assert logs[0].id == log2.id  # El més recent primer
        assert logs[1].id == log1.id


@pytest.mark.django_db
class TestSecurityEvent:
    """Tests per al model SecurityEvent"""

    def test_security_event_creation(self):
        """Test creació d'un event de seguretat"""
        event = SecurityEvent.objects.create(
            event_type="BRUTE_FORCE",
            ip_address="192.168.1.100",
            user_agent="Test Agent",
            description="Intent de força bruta",
            severity="HIGH",
        )

        assert event.event_type == "BRUTE_FORCE"
        assert event.ip_address == "192.168.1.100"
        assert event.severity == "HIGH"

    def test_security_event_with_user(self, api_user):
        """Test event de seguretat associat a usuari"""
        event = SecurityEvent.objects.create(
            event_type="UNAUTHORIZED_ACCESS",
            user=api_user,
            ip_address="10.0.0.1",
            description="Intent d'accés no autoritzat",
            severity="CRITICAL",
        )

        assert event.user == api_user
        assert event.severity == "CRITICAL"


@pytest.mark.django_db
class TestAuditSignals:
    """Tests per als signals d'auditoria"""

    def test_envio_creation_generates_audit_log(self, darp_user):
        """Test que crear un Envio genera un log d'auditoria"""
        from sales_notes.models import Envio

        initial_count = AuditLog.objects.count()

        Envio.objects.create(num_envio="TEST_001", tipo_respuesta=1, usuario_envio=darp_user)

        assert AuditLog.objects.count() == initial_count + 1

        log = AuditLog.objects.latest("timestamp")
        assert log.action == "CREATE"
        assert log.user == darp_user
        assert "TEST_001" in log.description

    def test_failed_login_generates_audit_log(self, api_client):
        """Test que un login fallit genera un log d'auditoria"""
        initial_count = AuditLog.objects.filter(action="FAILED_LOGIN").count()

        response = api_client.post(
            "/api/auth/token/", {"username": "nonexistent", "password": "wrongpassword"}, format="json"
        )

        assert response.status_code == 401
        assert AuditLog.objects.filter(action="FAILED_LOGIN").count() == initial_count + 1

        log = AuditLog.objects.filter(action="FAILED_LOGIN").latest("timestamp")
        assert log.severity == "WARNING"
        assert "nonexistent" in log.description


@pytest.mark.django_db
@pytest.mark.unit
class TestAuditTasks:
    """Tests per a les tasques d'auditoria"""

    def test_cleanup_old_logs_deletes_old_info_logs(self, api_user):
        """Test que cleanup_old_logs elimina logs INFO antics"""
        from audit.tasks import cleanup_old_logs

        # Crear log antic (>365 dies)
        old_date = timezone.now() - timedelta(days=400)
        old_log = AuditLog.objects.create(action="CREATE", user=api_user, description="Log antic", severity="INFO")
        old_log.timestamp = old_date
        old_log.save()

        # Crear log recent
        recent_log = AuditLog.objects.create(action="CREATE", user=api_user, description="Log recent", severity="INFO")

        initial_count = AuditLog.objects.count()

        # Executar tasca
        result = cleanup_old_logs()

        # Verificar que s'ha eliminat el log antic
        assert AuditLog.objects.count() == initial_count - 1
        assert not AuditLog.objects.filter(id=old_log.id).exists()
        assert AuditLog.objects.filter(id=recent_log.id).exists()
        assert result["deleted"] == 1

    def test_cleanup_old_logs_keeps_critical_logs(self, api_user):
        """Test que cleanup_old_logs manté logs CRITICAL antics"""
        from audit.tasks import cleanup_old_logs

        # Crear log CRITICAL antic
        old_date = timezone.now() - timedelta(days=400)
        critical_log = AuditLog.objects.create(
            action="DELETE", user=api_user, description="Eliminació crítica", severity="CRITICAL"
        )
        critical_log.timestamp = old_date
        critical_log.save()

        initial_count = AuditLog.objects.count()

        # Executar tasca
        cleanup_old_logs()

        # Verificar que el log CRITICAL NO s'ha eliminat
        assert AuditLog.objects.count() == initial_count
        assert AuditLog.objects.filter(id=critical_log.id).exists()

    def test_check_security_events_detects_brute_force(self):
        """Test que check_security_events detecta atacs de força bruta"""
        from audit.tasks import check_unresolved_security_events

        # Crear múltiples events de força bruta
        for i in range(7):
            SecurityEvent.objects.create(event_type="BRUTE_FORCE", ip_address=f"192.168.1.{i}", severity="HIGH")

        result = check_unresolved_security_events()

        assert result["total_events"] >= 7
        assert result["events_by_type"]["BRUTE_FORCE"] >= 7
        assert any("força bruta" in alert["message"].lower() for alert in result["alerts"])

    def test_check_security_events_detects_injections(self):
        """Test que check_security_events detecta intents d'injecció"""
        from audit.tasks import check_unresolved_security_events

        SecurityEvent.objects.create(event_type="SQL_INJECTION", ip_address="10.0.0.1", severity="CRITICAL")

        SecurityEvent.objects.create(event_type="XSS_ATTEMPT", ip_address="10.0.0.2", severity="CRITICAL")

        result = check_unresolved_security_events()

        assert result["critical_events"] >= 2
        assert any("injecció" in alert["message"].lower() for alert in result["alerts"])

    def test_check_security_events_no_alerts_when_empty(self):
        """Test que no genera alertes quan no hi ha events"""
        from audit.tasks import check_unresolved_security_events

        # Netejar tots els events recents
        SecurityEvent.objects.all().delete()

        result = check_unresolved_security_events()

        assert result["total_events"] == 0
        assert result["alerts"] == []
