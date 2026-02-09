"""
Configuració de seguretat per a entorn de PRODUCCIÓ

Aquest fitxer conté les configuracions de seguretat necessàries per passar
el Django security check en producció.

IMPORTANT: Aquestes configuracions només s'han d'aplicar en PRODUCCIÓ.
           En desenvolupament/testing poden causar problemes.

Per utilitzar aquestes configuracions:
1. Afegir al final de settings.py:
   if not DEBUG:
       from .settings_production import *

2. O crear un settings_production.py separat i usar:
   python manage.py runserver --settings=vcpe_api.settings_production
"""

# ==============================================================================
# SECURITY SETTINGS - NOMÉS PER PRODUCCIÓ
# ==============================================================================

# HSTS (HTTP Strict Transport Security)
# https://docs.djangoproject.com/en/5.1/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 31536000  # 1 any
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL/HTTPS Redirect
# Forçar totes les connexions a HTTPS
SECURE_SSL_REDIRECT = True

# Secure Proxy SSL Header
# Si utilitzeu un reverse proxy (nginx, load balancer)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Session Cookie Security
SESSION_COOKIE_SECURE = True  # Només enviar cookie per HTTPS
SESSION_COOKIE_HTTPONLY = True  # No accessible via JavaScript
SESSION_COOKIE_SAMESITE = "Lax"  # Protecció CSRF

# CSRF Cookie Security
CSRF_COOKIE_SECURE = True  # Només enviar cookie per HTTPS
CSRF_COOKIE_HTTPONLY = True  # No accessible via JavaScript
CSRF_COOKIE_SAMESITE = "Lax"

# Content Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevenir MIME type sniffing
SECURE_BROWSER_XSS_FILTER = True  # Activar XSS filter del navegador
X_FRAME_OPTIONS = "DENY"  # Prevenir clickjacking

# ==============================================================================
# CORS SETTINGS - RESTRINGIR EN PRODUCCIÓ
# ==============================================================================

# IMPORTANT: Canviar per als vostres dominis reals
CORS_ALLOWED_ORIGINS = [
    "https://vostredomini.cat",
    "https://app.vostredomini.cat",
]

CORS_ALLOW_CREDENTIALS = True

# Només permetre aquests mètodes HTTP
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ==============================================================================
# LOGGING - PRODUCCIÓ
# ==============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": "log_request_id.filters.RequestIDFilter",
        },
    },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(request_id)s %(message)s",
        },
        "verbose": {
            "format": "[{levelname}] {asctime} [{request_id}] {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/vcpe_api/django.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10,
            "formatter": "json",
            "filters": ["request_id"],
        },
        "security_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/vcpe_api/security.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 20,
            "formatter": "json",
            "filters": ["request_id"],
            "level": "WARNING",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console", "security_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "sales_notes": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "authentication": {
            "handlers": ["console", "file", "security_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

# ==============================================================================
# RATE LIMITING - PRODUCCIÓ
# ==============================================================================

# Activar rate limiting més estricte en producció
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"

# ==============================================================================
# DATABASE - OPTIMITZACIONS PRODUCCIÓ
# ==============================================================================

# Connexions persistents per millor rendiment
CONN_MAX_AGE = 600  # 10 minuts

# ==============================================================================
# STATIC & MEDIA FILES - PRODUCCIÓ
# ==============================================================================

# Servir fitxers estàtics via CDN o servidor web (nginx)
STATIC_ROOT = "/var/www/vcpe_api/static/"
MEDIA_ROOT = "/var/www/vcpe_api/media/"

# ==============================================================================
# EMAIL - PRODUCCIÓ
# ==============================================================================

# Configurar SMTP real en producció
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.vostredomini.cat'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'vostremail@vostredomini.cat'
# EMAIL_HOST_PASSWORD = 'password_des_del_.env'

# Admins per notificacions d'errors
ADMINS = [
    ("Admin Name", "admin@vostredomini.cat"),
]
MANAGERS = ADMINS

# ==============================================================================
# CACHE - PRODUCCIÓ
# ==============================================================================

# Usar Redis per cache en producció
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "vcpe_api",
        "TIMEOUT": 300,
    }
}

# ==============================================================================
# CELERY - PRODUCCIÓ
# ==============================================================================

# Configurar Celery per processos asíncrons en producció
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_ALWAYS_EAGER = False  # Executar tasques en background

# ==============================================================================
# DRF SPECTACULAR - PRODUCCIÓ
# ==============================================================================

# Protegir documentació API en producció
SPECTACULAR_SETTINGS = {
    "TITLE": "VCPE API",
    "DESCRIPTION": "API per gestió de notes de venda i captura",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # Deshabilitar /api/schema/ en producció
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],  # Només admins
}
