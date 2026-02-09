"""
Projecte VCPE API - Sistema de recepció de notes de venda
ICATMAR - Institut Català de Recerca per a la Governança del Mar
"""

# Assegurar que Celery s'inicialitza amb Django
from .celery import app as celery_app

__all__ = ("celery_app",)
__version__ = "1.0.0"
