"""
Configuració de Celery per tasques asíncrones i programades
"""

import os

from celery import Celery
from celery.schedules import crontab

# Establir el mòdul de configuració per defecte de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vcpe_api.settings")

app = Celery("vcpe_api")

# Usar la configuració de Django amb namespace 'CELERY'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks en totes les apps instal·lades
app.autodiscover_tasks()


# Configuració de tasques periòdiques
app.conf.beat_schedule = {
    # Processar enviaments pendents cada 5 minuts
    "process-pending-envios": {
        "task": "sales_notes.tasks.process_pending_envios",
        "schedule": crontab(minute="*/5"),
    },
    # Netejar logs antics cada dia a les 3 AM
    "cleanup-old-logs": {
        "task": "audit.tasks.cleanup_old_logs",
        "schedule": crontab(hour=3, minute=0),
    },
    # Generar informe diari d'estadístiques
    "daily-statistics-report": {
        "task": "sales_notes.tasks.generate_daily_report",
        "schedule": crontab(hour=7, minute=30),
    },
    # Comprovar events de seguretat no resolts cada hora
    "check-unresolved-security-events": {
        "task": "audit.tasks.check_unresolved_security_events",
        "schedule": crontab(minute=0),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tasca de debug per comprovar que Celery funciona"""
    print(f"Request: {self.request!r}")
