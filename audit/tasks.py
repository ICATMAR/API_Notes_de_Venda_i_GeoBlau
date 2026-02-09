"""
Tasques periòdiques d'auditoria amb Celery
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger("audit")


@shared_task
def cleanup_old_logs():
    """
    Neteja registres d'auditoria més antics de 365 dies
    Compliment RGPD Article 5.1.e - Limitació termini conservació
    """
    from audit.models import AuditLog

    cutoff_date = timezone.now() - timedelta(days=365)
    deleted_count, _ = AuditLog.objects.filter(
        timestamp__lt=cutoff_date, severity="INFO"  # Només INFO, mantenim WARNING/ERROR/CRITICAL més temps
    ).delete()

    logger.info(f"Netejats {deleted_count} registres d'auditoria anteriors a {cutoff_date}")
    return {"deleted": deleted_count, "cutoff_date": cutoff_date.isoformat()}


@shared_task
def check_unresolved_security_events(hours=1, brute_force_threshold=5, rate_limit_threshold=10):
    """
    Comprova events de seguretat no resolts i genera alertes

    Args:
        hours: Finestra temporal a analitzar (defecte: 1 hora)
        brute_force_threshold: Nombre d'intents per considerar atac (defecte: 5)
        rate_limit_threshold: Nombre de rate limits per alerta DoS (defecte: 10)
    """
    from audit.models import SecurityEvent

    cutoff_time = timezone.now() - timedelta(hours=hours)

    # Obtenir tots els events del període
    recent_events = SecurityEvent.objects.filter(timestamp__gte=cutoff_time)
    total_count = recent_events.count()

    if total_count == 0:
        logger.info(f"No s'han detectat events de seguretat en les últimes {hours} hora(es)")
        return {"period_hours": hours, "total_events": 0, "critical_events": 0, "alerts": []}

    # Definir categories de severitat
    CRITICAL_EVENT_TYPES = [
        "BRUTE_FORCE",
        "SQL_INJECTION",
        "XSS_ATTEMPT",
        "UNAUTHORIZED_ACCESS",
        "DATA_BREACH_ATTEMPT",
    ]

    HIGH_SEVERITY_TYPES = [
        "INVALID_TOKEN",
        "MALFORMED_REQUEST",
    ]

    # Análisi per tipus
    events_by_type = {}
    critical_count = 0
    high_severity_count = 0

    for event in recent_events:
        event_type = event.event_type
        events_by_type[event_type] = events_by_type.get(event_type, 0) + 1

        if event_type in CRITICAL_EVENT_TYPES:
            critical_count += 1
        elif event_type in HIGH_SEVERITY_TYPES:
            high_severity_count += 1

    # Generar alertes
    alerts = []

    # Alerta crítica
    if critical_count > 0:
        alerts.append(
            {
                "level": "CRITICAL",
                "message": f"{critical_count} events crítics de seguretat detectats",
                "types": [t for t in events_by_type.keys() if t in CRITICAL_EVENT_TYPES],
            }
        )

    # Detecció atac força bruta
    brute_force_count = events_by_type.get("BRUTE_FORCE", 0)
    if brute_force_count >= brute_force_threshold:
        alerts.append(
            {
                "level": "HIGH",
                "message": f"Possible atac de força bruta detectat: {brute_force_count} intents",
                "count": brute_force_count,
            }
        )

    # Detecció atac DoS
    rate_limit_count = events_by_type.get("RATE_LIMIT_EXCEEDED", 0)
    if rate_limit_count >= rate_limit_threshold:
        alerts.append(
            {
                "level": "HIGH",
                "message": f"Possible atac DoS detectat: {rate_limit_count} límits excedits",
                "count": rate_limit_count,
            }
        )

    # Detecció injeccions
    injection_count = events_by_type.get("SQL_INJECTION", 0) + events_by_type.get("XSS_ATTEMPT", 0)
    if injection_count > 0:
        alerts.append(
            {
                "level": "CRITICAL",
                "message": f"Intents d'injecció detectats: {injection_count}",
                "count": injection_count,
            }
        )

    # Logging segons severitat
    if any(a["level"] == "CRITICAL" for a in alerts):
        logger.critical(
            f"🚨 ALERTES CRÍTIQUES DE SEGURETAT (últimes {hours}h): "
            f"{[a['message'] for a in alerts if a['level'] == 'CRITICAL']}. "
            f"Events per tipus: {events_by_type}"
        )
    elif alerts:
        logger.warning(
            f"⚠️ Alertes de seguretat (últimes {hours}h): "
            f"{[a['message'] for a in alerts]}. "
            f"Events per tipus: {events_by_type}"
        )
    else:
        logger.info(
            f"✅ Events de seguretat sota control (últimes {hours}h). "
            f"Total: {total_count}, Detall: {events_by_type}"
        )

    return {
        "period_hours": hours,
        "total_events": total_count,
        "critical_events": critical_count,
        "high_severity_events": high_severity_count,
        "events_by_type": events_by_type,
        "alerts": alerts,
        "thresholds": {"brute_force": brute_force_threshold, "rate_limit": rate_limit_threshold},
    }
