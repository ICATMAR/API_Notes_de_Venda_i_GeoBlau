# ============================================
# sales_notes/__init__.py
# ============================================
default_app_config = 'sales_notes.apps.SalesNotesConfig'


# ============================================
# sales_notes/apps.py
# ============================================
from django.apps import AppConfig


class SalesNotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_notes'
    verbose_name = 'Notes de Venda'


# ============================================
# authentication/__init__.py
# ============================================
default_app_config = 'authentication.apps.AuthenticationConfig'


# ============================================
# authentication/apps.py
# ============================================
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    verbose_name = 'Autenticació'


# ============================================
# audit/__init__.py
# ============================================
default_app_config = 'audit.apps.AuditConfig'


# ============================================
# audit/apps.py
# ============================================
from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit'
    verbose_name = 'Auditoria i Seguretat'
    
    def ready(self):
        """Importar signals quan l'app estigui llesta"""
        import audit.signals