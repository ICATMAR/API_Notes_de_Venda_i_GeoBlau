"""
Models per auditoria i traçabilitat del sistema
"""

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    """
    Registre d'auditoria per totes les operacions crítiques
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Informació d'acció
    ACTION_CHOICES = [
        ("CREATE", "Creació"),
        ("UPDATE", "Actualització"),
        ("DELETE", "Eliminació"),
        ("READ", "Lectura"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("FAILED_LOGIN", "Intent login fallit"),
        ("VALIDATION_ERROR", "Error de validació"),
        ("SECURITY_EVENT", "Event de seguretat"),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES, db_index=True)

    # Usuari que fa l'acció
    user = models.ForeignKey(
        "authentication.APIUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs"
    )

    # Objecte afectat (GenericForeignKey per referir qualsevol model)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # Detalls de l'acció
    description = models.TextField(help_text="Descripció de l'acció")

    # Dades abans i després (per UPDATE)
    old_value = models.JSONField(null=True, blank=True, help_text="Valor anterior (per actualitzacions)")
    new_value = models.JSONField(null=True, blank=True, help_text="Valor nou (per creacions i actualitzacions)")

    # Context de la petició
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_id = models.CharField(max_length=50, db_index=True, blank=True)

    # Severitat
    SEVERITY_CHOICES = [
        ("INFO", "Informació"),
        ("WARNING", "Avís"),
        ("ERROR", "Error"),
        ("CRITICAL", "Crític"),
    ]

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="INFO", db_index=True)

    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-timestamp"]
        verbose_name = "Registre d'auditoria"
        verbose_name_plural = "Registres d'auditoria"
        indexes = [
            models.Index(fields=["action", "timestamp"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["severity", "timestamp"]),
            models.Index(fields=["ip_address", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"


class SecurityEvent(models.Model):
    """
    Events de seguretat específics que requereixen atenció
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    EVENT_TYPE_CHOICES = [
        ("BRUTE_FORCE", "Intent de força bruta"),
        ("SQL_INJECTION", "Intent d'injecció SQL"),
        ("XSS_ATTEMPT", "Intent de XSS"),
        ("INVALID_TOKEN", "Token invàlid"),
        ("RATE_LIMIT_EXCEEDED", "Límit de peticions excedit"),
        ("UNAUTHORIZED_ACCESS", "Accés no autoritzat"),
        ("SUSPICIOUS_ACTIVITY", "Activitat sospitosa"),
        ("DATA_BREACH_ATTEMPT", "Intent de filtrament de dades"),
        ("MALFORMED_REQUEST", "Petició mal formada"),
    ]

    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, db_index=True)

    # Qui/què ho va originar
    user = models.ForeignKey(
        "authentication.APIUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="security_events"
    )

    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(blank=True)

    # Detalls de l'event
    description = models.TextField()
    request_path = models.CharField(max_length=500)
    request_method = models.CharField(max_length=10)
    request_data_hash = models.CharField(max_length=64, blank=True)

    # Resposta del sistema
    blocked = models.BooleanField(default=False, help_text="Si l'acció va ser bloquejada")

    action_taken = models.TextField(blank=True, help_text="Acció que va prendre el sistema")

    # Severitat i estat
    SEVERITY_CHOICES = [
        ("LOW", "Baixa"),
        ("MEDIUM", "Mitjana"),
        ("HIGH", "Alta"),
        ("CRITICAL", "Crítica"),
    ]

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="MEDIUM", db_index=True)

    STATUS_CHOICES = [
        ("NEW", "Nou"),
        ("INVESTIGATING", "En investigació"),
        ("RESOLVED", "Resolt"),
        ("FALSE_POSITIVE", "Fals positiu"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW", db_index=True)

    # Notificació
    notified = models.BooleanField(default=False, help_text="Si s'ha notificat als responsables")

    notified_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        "authentication.APIUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_security_events",
    )

    class Meta:
        db_table = "security_event"
        ordering = ["-timestamp"]
        verbose_name = "Event de seguretat"
        verbose_name_plural = "Events de seguretat"
        indexes = [
            models.Index(fields=["event_type", "timestamp"]),
            models.Index(fields=["severity", "status"]),
            models.Index(fields=["ip_address", "timestamp"]),
            models.Index(fields=["blocked", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.severity} ({self.timestamp})"


class DataValidationError(models.Model):
    """
    Errors de validació de dades per anàlisi i millora contínua
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    envio = models.ForeignKey("sales_notes.Envio", on_delete=models.CASCADE, related_name="validation_errors")

    # Camp i error
    field_name = models.CharField(max_length=100, db_index=True, help_text="Nom del camp amb error")

    error_type = models.CharField(max_length=50, db_index=True, help_text="Tipus d'error (ex: required, format, range)")

    error_message = models.TextField(help_text="Missatge d'error detallat")

    # Valor que va causar l'error
    invalid_value = models.TextField(blank=True, help_text="Valor que no va passar la validació")

    expected_format = models.TextField(blank=True, help_text="Format esperat")

    # Context
    json_path = models.CharField(max_length=500, blank=True, help_text="Path JSON on es troba l'error")

    # Resolució
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "data_validation_error"
        ordering = ["-timestamp"]
        verbose_name = "Error de validació"
        verbose_name_plural = "Errors de validació"
        indexes = [
            models.Index(fields=["field_name", "error_type"]),
            models.Index(fields=["resolved", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.field_name}: {self.error_type} ({self.envio.num_envio})"
