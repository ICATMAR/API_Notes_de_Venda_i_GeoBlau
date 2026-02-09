"""
Configuració de l'aplicació audit
"""

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Configuració de l'app d'auditoria i seguretat"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "audit"
    verbose_name = "Auditoria i Seguretat"

    def ready(self):
        """
        Importar signals quan l'app estigui llesta
        Això activa el sistema d'auditoria automàtica
        """
        import audit.signals  # noqa: F401
