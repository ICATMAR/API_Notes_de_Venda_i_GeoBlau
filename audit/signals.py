"""
Signals per auditoria automàtica de canvis en models crítics
"""

import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from audit.models import AuditLog
from authentication.models import User
from sales_notes.models import Envio

logger = logging.getLogger("audit")


@receiver(post_save, sender=Envio)
def audit_envio_created(sender, instance, created, **kwargs):
    """Auditar creació d'enviaments"""
    if created:
        # No capturem excepcions aquí per evitar trencar transaccions atòmiques silenciosament.
        # Si falla l'auditoria, ha de fallar la creació de l'enviament.
        AuditLog.objects.create(
            action="CREATE",
            user=instance.usuario_envio,
            content_object=instance,
            description=f"Creat enviament {instance.num_envio}",
            new_value={"num_envio": instance.num_envio, "fecha_recepcion": instance.fecha_recepcion.isoformat()},
            severity="INFO",
        )
        logger.info(f"Auditat creació d'enviament {instance.num_envio}")


@receiver(user_logged_in)
def audit_user_login(sender, request, user, **kwargs):
    """Auditar login exitós"""
    try:
        ip_address = request.META.get("REMOTE_ADDR")

        # Actualitzar última IP de login i restablir comptador d'intents fallits
        try:
            user.record_successful_login(ip_address=ip_address)
        except Exception:
            logger.exception("Error actualitzant l'estat d'usuari després de login exitós")

        # Ara crear el log d'event 'LOGIN' — ha de ser el més recent
        try:
            AuditLog.objects.create(
                action="LOGIN",
                user=user,
                description=f"Login exitós de {user.username}",
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                severity="INFO",
            )
        except Exception:
            logger.exception("Error creant AuditLog de LOGIN")

        logger.info(f"Login exitós: {user.username} des de {ip_address}")
    except Exception as e:
        logger.error(f"Error auditant login: {str(e)}", exc_info=True)


@receiver(user_logged_out)
def audit_user_logout(sender, request, user, **kwargs):
    """Auditar logout"""
    try:
        AuditLog.objects.create(
            action="LOGOUT",
            user=user,
            description=f"Logout de {user.username}",
            ip_address=request.META.get("REMOTE_ADDR") if request else None,
            severity="INFO",
        )
        logger.info(f"Logout: {user.username}")
    except Exception as e:
        logger.error(f"Error auditant logout: {str(e)}", exc_info=True)


@receiver(user_login_failed)
def audit_failed_login(sender, credentials, request, **kwargs):
    """Auditar intents de login fallits"""
    try:
        username = credentials.get("username", "Unknown")
        ip_address = request.META.get("REMOTE_ADDR") if request else None

        AuditLog.objects.create(
            action="FAILED_LOGIN",
            description=f"Intent de login fallit per {username}",
            ip_address=ip_address,
            user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
            severity="WARNING",
        )

        # Incrementar contador d'intents fallits si l'usuari existeix
        try:
            user = User.objects.get(username=username)
            user.record_failed_login()
        except User.DoesNotExist:
            pass

        logger.warning(f"Intent de login fallit: {username} des de {ip_address}")
    except Exception as e:
        logger.error(f"Error auditant login fallit: {str(e)}", exc_info=True)


@receiver(post_save, sender=User)
def audit_user_changes(sender, instance, created, **kwargs):
    """Auditar canvis en usuaris"""
    try:
        if created:
            AuditLog.objects.create(
                action="CREATE",
                content_object=instance,
                description=f"Creat usuari {instance.username}",
                new_value={"username": instance.username},
                severity="INFO",
            )
        else:
            # Evitar soroll: Si només s'actualitza el last_login, és part del procés de login
            # i ja es genera un log específic d'acció "LOGIN".
            update_fields = kwargs.get("update_fields")
            if update_fields and "last_login" in update_fields and len(update_fields) == 1:
                return

            # Per actualitzacions, només registrar si hi ha canvis importants
            # (això requeriria guardar l'estat anterior, es pot fer amb django-dirtyfields)
            AuditLog.objects.create(
                action="UPDATE",
                content_object=instance,
                description=f"Actualitzat usuari {instance.username}",
                severity="INFO",
            )
    except Exception as e:
        logger.error(f"Error auditant usuari: {str(e)}", exc_info=True)


@receiver(post_delete, sender=Envio)
def audit_envio_deleted(sender, instance, **kwargs):
    """Auditar eliminació d'enviaments (molt crític!)"""
    try:
        AuditLog.objects.create(
            action="DELETE",
            description=f"ELIMINAT enviament {instance.num_envio}",
            old_value={
                "num_envio": instance.num_envio,
                "fecha_recepcion": instance.fecha_recepcion.isoformat(),
            },
            severity="CRITICAL",
        )
        logger.critical(f"ELIMINAT enviament {instance.num_envio}")
    except Exception as e:
        logger.error(f"Error auditant eliminació: {str(e)}", exc_info=True)
