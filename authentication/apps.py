"""
Configuració de l'aplicació authentication
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuració de l'app d'autenticació"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
    verbose_name = "Autenticació i Usuaris API"

    def ready(self):
        """
        Mètode executat quan l'aplicació està llesta
        """
        pass  # Els signals es registren des de audit.signals
