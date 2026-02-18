import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Model d'usuari personalitzat que mapeja a la taula 'auth_user' existent.
    Utilitzem managed = False per no alterar l'esquema de la BD legacy.
    """

    # Redefinim first_name perquè a la BD legacy és de 30 caràcters (Django modern usa 150)
    first_name = models.CharField("first name", max_length=30, blank=True)

    # Nota: En canviar el nom de la classe a 'User', Django utilitzarà per defecte
    # 'user_id' com a clau forana en les relacions M2M, que és exactament
    # el que necessitem per a les taules existents auth_user_groups i auth_user_user_permissions.
    # No cal redefinir groups ni user_permissions manualment.

    # Mètodes helpers per compatibilitat amb el codi existent (views.py)
    # Retornen valors per defecte perquè la taula legacy no té aquests camps
    def is_account_locked(self):
        """Sempre retorna False perquè no gestionem bloqueig a la BD legacy."""
        return False

    def record_failed_login(self):
        """No fem res perquè no tenim on guardar els intents fallits."""
        pass

    def record_successful_login(self, ip_address=None):
        """
        Actualitza només la data de l'últim login (camp existent a auth_user).
        """
        # Actualitzar last_login a la taula legacy
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    class Meta:
        # CRUCIAL: managed = False evita que Django intenti modificar la taula 'auth_user' existent
        managed = False
        db_table = "auth_user"
        verbose_name = "Usuari"
        verbose_name_plural = "Usuaris"


class APIAccessLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="access_logs")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255, db_index=True)
    query_params = models.TextField(blank=True, null=True)
    status_code = models.IntegerField()
    user_agent = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.FloatField(null=True, blank=True)
    request_id = models.CharField(max_length=100, blank=True, default="")
    request_body_hash = models.CharField(max_length=64, blank=True, default="")
    error_message = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = _("API Access Log")
        verbose_name_plural = _("API Access Logs")
