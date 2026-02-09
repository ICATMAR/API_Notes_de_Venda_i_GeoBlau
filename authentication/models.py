"""
Models per gestió d'usuaris i autenticació de l'API
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class APIUser(AbstractUser):
    """
    Usuari personalitzat per l'API amb camps addicionals de seguretat
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Informació organització
    organization = models.CharField(
        max_length=200, help_text="Nom de l'organització (ex: Confraria de pescadors, llotja)"
    )

    cif_organization = models.CharField(max_length=20, help_text="CIF de l'organització")

    is_locked = models.BooleanField(default=False, help_text="Indica si el compte està bloquejat per seguretat")

    locked_until = models.DateTimeField(null=True, blank=True, help_text="Data fins quan està bloquejat el compte")

    lock_reason = models.CharField(max_length=255, blank=True, help_text="Raó del bloqueig del compte")

    last_failed_login = models.DateTimeField(null=True, blank=True, help_text="Data de l'últim intent de login fallit")

    password_changed_at = models.DateTimeField(null=True, blank=True, help_text="Data de l'últim canvi de contrasenya")

    must_change_password = models.BooleanField(
        default=False, help_text="Indica si l'usuari ha de canviar la contrasenya al proper login"
    )

    # Contacte
    telefono = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(regex=r"^\+?1?\d{9,15}$", message="Número de telèfon invàlid")],
    )

    # Seguretat i control d'accés
    is_api_active = models.BooleanField(default=True, help_text="Indica si l'usuari pot accedir a l'API")

    api_key = models.CharField(
        max_length=64, unique=True, blank=True, null=True, help_text="API Key per autenticació addicional (opcional)"
    )

    # Límits i quotes
    max_requests_per_day = models.IntegerField(default=10000, help_text="Màxim de peticions per dia")

    max_requests_per_hour = models.IntegerField(default=1000, help_text="Màxim de peticions per hora")

    # Whitelisting d'IPs
    allowed_ips = models.JSONField(default=list, blank=True, help_text="Llista d'IPs permeses (buit = totes)")

    # Audit de seguretat AMPLIAT
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, help_text="IP de l'últim login exitós")

    failed_login_attempts = models.IntegerField(default=0, help_text="Nombre d'intents de login fallits consecutius")

    account_locked_until = models.DateTimeField(
        null=True, blank=True, help_text="Data fins quan està bloquejat el compte"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_user"
        verbose_name = "Usuari API"
        verbose_name_plural = "Usuaris API"
        indexes = [
            models.Index(fields=["cif_organization"]),
            models.Index(fields=["is_api_active", "is_active"]),
        ]

    def __str__(self):
        return f"{self.username} - {self.organization}"

    def is_account_locked(self):
        """
        Verifica si el compte està bloquejat
        Desbloqueja automàticament si ha passat el temps
        """
        if self.account_locked_until and timezone.now() > self.account_locked_until:
            self.failed_login_attempts = 0
            self.account_locked_until = None
            self.save(update_fields=["failed_login_attempts", "account_locked_until"])
            return False
        return self.account_locked_until is not None

    def record_failed_login(self):
        """Registra un intent de login fallit i bloqueja si cal"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=15)
        self.save(update_fields=["failed_login_attempts", "account_locked_until"])

    def record_successful_login(self, ip_address=None):
        """Registra un login exitós"""
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=["last_login_ip", "failed_login_attempts", "account_locked_until"])


class APIAccessLog(models.Model):
    """
    Log d'accessos a l'API per auditoria
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(APIUser, on_delete=models.SET_NULL, null=True, related_name="access_logs")

    endpoint = models.CharField(max_length=500)
    method = models.CharField(max_length=10)

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)

    request_id = models.CharField(max_length=50, db_index=True)

    status_code = models.IntegerField()
    response_time_ms = models.IntegerField(help_text="Temps de resposta en ms")

    request_body_hash = models.CharField(max_length=64, blank=True, help_text="Hash SHA256 del body (per privacitat)")

    error_message = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "api_access_log"
        ordering = ["-timestamp"]
        verbose_name = "Log d'accés API"
        verbose_name_plural = "Logs d'accés API"
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["ip_address", "timestamp"]),
            models.Index(fields=["status_code", "timestamp"]),
            models.Index(fields=["request_id"]),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code} ({self.timestamp})"


class AuthenticationToken(models.Model):
    """
    Model per gestionar tokens JWT amb auditoria completa i revocació
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        APIUser, on_delete=models.CASCADE, related_name="authentication_tokens", verbose_name=_("user")
    )

    # Token identification
    jti = models.CharField(
        _("JWT ID"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Unique identifier for the JWT token (jti claim)"),
    )

    token_type = models.CharField(
        _("token type"),
        max_length=20,
        choices=[
            ("access", _("Access Token")),
            ("refresh", _("Refresh Token")),
        ],
        default="access",
    )

    # Token lifecycle
    issued_at = models.DateTimeField(_("issued at"), auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(_("expires at"), db_index=True)

    # Revocation management
    is_revoked = models.BooleanField(_("revoked"), default=False, db_index=True)
    revoked_at = models.DateTimeField(_("revoked at"), null=True, blank=True)
    revoked_by = models.ForeignKey(
        APIUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revoked_tokens",
        verbose_name=_("revoked by"),
    )
    revocation_reason = models.CharField(_("revocation reason"), max_length=255, blank=True)

    # Request context
    ip_address = models.GenericIPAddressField(_("IP address"))
    user_agent = models.TextField(_("user agent"), blank=True)

    class Meta:
        db_table = "auth_token"
        verbose_name = _("authentication token")
        verbose_name_plural = _("authentication tokens")
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["user", "is_revoked", "expires_at"]),
            models.Index(fields=["jti", "is_revoked"]),
        ]

    def __str__(self):
        return f"{self.get_token_type_display()} - {self.user.username} - {self.jti[:8]}"

    def is_valid(self):
        """Check if the token is currently valid"""
        if self.is_revoked:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True

    def revoke(self, revoked_by=None, reason=""):
        """Revoke the token"""
        self.is_revoked = True
        self.revoked_at = timezone.now()
        self.revoked_by = revoked_by
        self.revocation_reason = reason
        self.save(update_fields=["is_revoked", "revoked_at", "revoked_by", "revocation_reason"])


class AuthenticationAuditLog(models.Model):
    """
    Log d'auditoria específic per events d'autenticació
    Compleix requisits GDPR i OWASP de logging
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        APIUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authentication_audit_logs",
        verbose_name=_("user"),
    )

    # Event classification
    EVENT_TYPES = [
        ("LOGIN_SUCCESS", _("Successful login")),
        ("LOGIN_FAILED", _("Failed login attempt")),
        ("LOGIN_BLOCKED", _("Login blocked due to account lock")),
        ("LOGOUT", _("User logout")),
        ("TOKEN_ISSUED", _("JWT token issued")),
        ("TOKEN_REFRESHED", _("JWT token refreshed")),
        ("TOKEN_REVOKED", _("JWT token revoked")),
        ("TOKEN_EXPIRED", _("Expired token used")),
        ("PASSWORD_CHANGED", _("Password changed")),
        ("ACCOUNT_LOCKED", _("Account locked")),
        ("ACCOUNT_UNLOCKED", _("Account unlocked")),
    ]

    event_type = models.CharField(_("event type"), max_length=30, choices=EVENT_TYPES, db_index=True)

    # Event context
    ip_address = models.GenericIPAddressField(_("IP address"))
    user_agent = models.TextField(_("user agent"), blank=True)
    username_attempted = models.CharField(_("attempted username"), max_length=150, blank=True)

    # Additional details
    details = models.JSONField(_("event details"), default=dict, blank=True)

    # Severity classification
    SEVERITY_LEVELS = [
        ("INFO", _("Information")),
        ("WARNING", _("Warning")),
        ("ERROR", _("Error")),
        ("CRITICAL", _("Critical")),
    ]

    severity = models.CharField(_("severity"), max_length=10, choices=SEVERITY_LEVELS, default="INFO", db_index=True)

    # Timestamp
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True, db_index=True)

    class Meta:
        db_table = "auth_audit_log"
        verbose_name = _("authentication audit log")
        verbose_name_plural = _("authentication audit logs")
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["event_type", "timestamp"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["severity", "timestamp"]),
            models.Index(fields=["ip_address", "timestamp"]),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else self.username_attempted or "Unknown"
        return f"{self.get_event_type_display()} - {user_str} - {self.timestamp}"

    @classmethod
    def log_event(
        cls, event_type, ip_address, user=None, username_attempted="", user_agent="", details=None, severity="INFO"
    ):
        """Create an audit log entry"""
        return cls.objects.create(
            event_type=event_type,
            user=user,
            username_attempted=username_attempted,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
            severity=severity,
        )
