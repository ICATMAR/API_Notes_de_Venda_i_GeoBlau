"""
Configuració de l'aplicació sales_notes
"""

from django.apps import AppConfig


class SalesNotesConfig(AppConfig):
    """Configuració de l'app de notes de venda"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sales_notes"
    verbose_name = "Notes de Venda"

    def ready(self):
        """
        Mètode executat quan l'aplicació està llesta
        Importar signals si n'hi ha
        """
        pass  # Els signals s'importen des de audit.apps.AuditConfig
