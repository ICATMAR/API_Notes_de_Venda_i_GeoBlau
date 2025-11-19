"""
Database Router per compartir taules Django core (public)
i crear només les específiques del projecte (api_dev)

Col·loca aquest fitxer a: vcpe_api/db_router.py
"""


class SchemaRouter:
    """
    Router que:
    - Usa taules Django core de 'public' (ja existents)
    - Crea taules del projecte a 'api_dev'
    """

    # Apps de Django core que ja existeixen a public
    DJANGO_CORE_APPS = {
        "admin",
        "auth",  # auth_user, auth_group, auth_permission
        "contenttypes",  # django_content_type
        "sessions",  # django_session
    }

    # Apps del teu projecte que van a api_dev
    PROJECT_APPS = {
        "sales_notes",
        "authentication",
        "audit",
    }

    def db_for_read(self, model, **hints):
        """Totes les lectures van a 'default'"""
        return "default"

    def db_for_write(self, model, **hints):
        """Totes les escriptures van a 'default'"""
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permetre relacions entre objectes
        Important: pots relacionar models de api_dev amb auth.User (public)
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Decisió clau: quines apps es migren i quines no

        - Apps Django core: NO es migren (ja existeixen a public)
        - Apps del projecte: SÍ es migren (es creen a api_dev)
        """
        if db != "default":
            return False

        # Apps de Django core: NO migrar (ja existeixen a public)
        if app_label in self.DJANGO_CORE_APPS:
            return False

        # Apps del projecte: SÍ migrar (crear a api_dev)
        if app_label in self.PROJECT_APPS:
            return True

        # Per defecte, permetre migracions
        return None
