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
        "total_envios": Envio.objects.filter(fecha_recepcion__gte=yesterday, fecha_recepcion__lt=today).count(),
        "by_tipo_respuesta": {},
    }

    for tipo in [1, 2, 3]:
        count = Envio.objects.filter(
            fecha_recepcion__gte=yesterday, fecha_recepcion__lt=today, tipo_respuesta=tipo
        ).count()
        stats["by_tipo_respuesta"][tipo] = count

    logger.info(f"Estadístiques diàries: {stats}")
    return stats


@shared_task
def process_pending_envios():
    """
    Processa enviaments pendents de validació completa
    Preparat per futures validacions amb ML
    """
    from sales_notes.models import Envio

    pending = Envio.objects.filter(procesado=False, validado=False)[:100]  # Processar màxim 100 per batch

    processed_count = 0
    for envio in pending:
        # TODO: Aquí aniria la validació ML de "sonso"
        envio.procesado = True
        envio.save(update_fields=["procesado"])
        processed_count += 1

    logger.info(f"Processats {processed_count} enviaments pendents")
    return {"processed": processed_count}
