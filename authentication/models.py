"""
Models per gestió d'usuaris i autenticació de l'API
"""

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
import uuid


class APIUser(models.Model):
    """
    Perfil d'usuari per l'API
    Relacionat amb auth_user de public (esquema compartit)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relació amb l'usuari de Django (a public.auth_user)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='api_profile',
        help_text="Usuari del sistema (auth_user de public)"
    )
    
    # Informació organització
    organizacion = models.CharField(
        max_length=200,
        help_text="Nom de l'organització (ex: Confraria de pescadors, llotja)"
    )
    
    cif_organizacion = models.CharField(
        max_length=20,
        unique=True,
        help_text="CIF de l'organització"
    )
    
    # Contacte
    telefono = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Número de telèfon invàlid'
            )
        ]
    )
    
    # Seguretat i control d'accés API
    is_api_active = models.BooleanField(
        default=True,
        help_text="Indica si l'usuari pot accedir a l'API"
    )
    
    api_key = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        null=True,
        help_text="API Key per autenticació addicional (opcional)"
    )
    
    # Límits i quotes
    max_requests_per_day = models.IntegerField(
        default=10000,
        help_text="Màxim de peticions per dia"
    )
    
    max_requests_per_hour = models.IntegerField(
        default=1000,
        help_text="Màxim de peticions per hora"
    )
    
    # Restriccions d'accés
    allowed_ips = models.JSONField(
        default=list,
        blank=True,
        help_text="Llista d'IPs permeses (buit = totes)"
    )
    
    # Tracking de seguretat
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'api_user'
        verbose_name = "Usuari API"
        verbose_name_plural = "Usuaris API"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['cif_organizacion']),
            models.Index(fields=['is_api_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.organizacion}"
    
    @property
    def is_active(self):
        """L'usuari està actiu si ho està a Django i a l'API"""
        return self.user.is_active and self.is_api_active
    
    def can_access_api(self, ip_address=None):
        """
        Comprova si l'usuari pot accedir a l'API
        """
        if not self.is_active:
            return False
        
        if self.account_locked_until:
            from django.utils import timezone
            if timezone.now() < self.account_locked_until:
                return False
            self.account_locked_until = None
            self.failed_login_attempts = 0
            self.save()
        
        if self.allowed_ips and ip_address:
            if ip_address not in self.allowed_ips:
                return False
        
        return True
    
    def increment_failed_login(self):
        """Incrementar intents fallits de login"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            from django.utils import timezone
            from datetime import timedelta
            self.account_locked_until = timezone.now() + timedelta(minutes=30)
        self.save()
    
    def reset_failed_login(self):
        """Reset després d'un login correcte"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save()


class APIAccessLog(models.Model):
    """
    Log d'accessos a l'API per auditoria
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        User,  # Directament a auth_user de public
        on_delete=models.SET_NULL,
        null=True,
        related_name='api_access_logs'
    )
    
    endpoint = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    request_id = models.CharField(max_length=50, db_index=True)
    
    status_code = models.IntegerField()
    response_time_ms = models.IntegerField(help_text="Temps de resposta en ms")
    
    request_body_hash = models.CharField(
        max_length=64,
        blank=True,
        help_text="Hash SHA256 del body (per privacitat)"
    )
    error_message = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'api_access_log'
        verbose_name = "Log d'accés API"
        verbose_name_plural = "Logs d'accés API"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
            models.Index(fields=['status_code', 'timestamp']),
        ]
    
    def __str__(self):
        username = self.user.username if self.user else "anonymous"
        return f"{username} - {self.method} {self.endpoint} - {self.status_code}"