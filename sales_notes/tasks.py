"""
Tasques periòdiques per gestió de notes de venda
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger("sales_notes")


@shared_task
def generate_daily_report():
    """
    Genera estadístiques diàries d'ús de l'API
    Útil per monitorització i detecció d'anomalies
    """
    from sales_notes.models import Envio

    yesterday = timezone.now() - timedelta(days=1)
    today = timezone.now()

    stats = {
        "date": yesterday.date().isoformat(),
        "total_envios_staging": Envio.objects.filter(fecha_recepcion__gte=yesterday, fecha_recepcion__lt=today).count(),
    }

    logger.info(f"Estadístiques diàries: {stats}")
    return stats
