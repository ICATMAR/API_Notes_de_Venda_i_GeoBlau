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
    o si hi ha enviaments encallats (no processats pel trigger),
    envia un correu d'alerta als administradors definits a settings.py.
    """

    from sales_notes.models import Envio

    one_day_ago = timezone.now() - timedelta(days=1)

    envios_count = Envio.objects.filter(fecha_recepcion__gte=one_day_ago).count()
    failed_envios = Envio.objects.filter(fecha_recepcion__gte=one_day_ago, procesado_en_db=False).count()

    alerts = []

    if envios_count == 0:
        alerts.append(
            {
                "subject": "[VCPE API ALERTA] Cap enviament rebut en les últimes 24 hores",
                "message": (
                    "El sistema de monitorització automàtica ha detectat que no s'ha rebut cap enviament "
                    "de notes de venda en les últimes 24 hores.\n\n"
                    "Això podria indicar un problema amb el client d'enviament (DARP) o la connectivitat.\n\n"
                    "Si us plau, verifiqueu l'estat del servei."
                ),
            }
        )
    elif failed_envios > 0:
        alerts.append(
            {
                "subject": f"[VCPE API ALERTA] {failed_envios} enviaments NO processats",
                "message": (
                    f"El sistema ha detectat que hi ha {failed_envios} enviament(s) rebut(s) en les últimes 24 hores "
                    "que no s'han processat correctament a la base de dades (procesado_en_db=False).\n\n"
                    "Això indica que el trigger de PostgreSQL pot haver fallat o trobat dades anòmales.\n"
                    "Consulteu la taula 'db_trigger_log' de la base de dades per a més detalls."
                ),
            }
        )

    if alerts:
        from django.conf import settings
        from django.core.mail import get_connection, send_mail

        recipients = (
            [a[1] for a in settings.NOTIFICATION_EMAIL]
            if getattr(settings, "NOTIFICATION_EMAIL", None)
            else ["arampuig.work@gmail.com"]
        )

        try:
            with get_connection(fail_silently=False) as connection:
                for alert in alerts:
                    logger.warning(alert["subject"])
                    send_mail(
                        alert["subject"],
                        alert["message"],
                        settings.DEFAULT_FROM_EMAIL,
                        recipients,
                        connection=connection,
                    )
            logger.info("Emails d'alerta enviats correctament.")
        except Exception as e:
            logger.error(f"❌ Error CRÍTIC enviant mail d'alerta: {e}")

        return f"Alertes enviades: {len(alerts)} incidències detectades."
    else:
        log_message = f"Activitat diària normal: {envios_count} enviaments rebuts i processats en les últimes 24h."
        logger.info(log_message)
        return log_message
