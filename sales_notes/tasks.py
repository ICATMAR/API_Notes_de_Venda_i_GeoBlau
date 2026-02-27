"""
Tasques periòdiques per gestió de notes de venda
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger("sales_notes")


@shared_task
def check_daily_activity_and_report_anomalies():
    """
    Verifica l'activitat diària. Si no hi ha hagut enviaments en 24h,
    envia un correu d'alerta als administradors definits a settings.py.
    """

    from sales_notes.models import Envio

    one_day_ago = timezone.now() - timedelta(days=1)

    envios_count = Envio.objects.filter(fecha_recepcion__gte=one_day_ago).count()

    if envios_count == 0:
        subject = "[VCPE API ALERTA] Cap enviament rebut en les últimes 24 hores"
        message = (
            "El sistema de monitorització automàtica ha detectat que no s'ha rebut cap enviament "
            "de notes de venda en les últimes 24 hores.\n\n"
            "Això podria indicar un problema amb el client d'enviament (DARP) o la connectivitat.\n\n"
            "Si us plau, verifiqueu l'estat del servei."
        )
        logger.warning(subject)
        # Aquesta funció envia un correu a tots els usuaris a la llista ADMINS de settings.py
        from django.conf import settings
        from django.core.mail import get_connection, send_mail

        recipients = [a[1] for a in settings.ADMINS] if getattr(settings, "ADMINS", None) else ["apuig@icatmar.cat"]

        try:
            with get_connection(fail_silently=False) as connection:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, connection=connection)
            logger.info("Email d'alerta enviat correctament.")
        except Exception as e:
            logger.error(f"❌ Error CRÍTIC enviant mail d'alerta: {e}")

        return "Alerta enviada: 0 enviaments rebuts en 24h."
    else:
        log_message = f"Activitat diària normal: {envios_count} enviaments rebuts en les últimes 24h."
        logger.info(log_message)
        return log_message
