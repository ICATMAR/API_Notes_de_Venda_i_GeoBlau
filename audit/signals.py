"""
Signals per auditoria automàtica de canvis en models crítics
"""

import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from audit.models import AuditLog
from authentication.models import APIUser
from sales_notes.models import Envio

logger = logging.getLogger("audit")


@receiver(post_save, sender=Envio)
def audit_envio_created(sender, instance, created, **kwargs):
    """Auditar creació d'enviaments"""
    if created:
        try:
            AuditLog.objects.create(
                action="CREATE",
                user=instance.usuario_envio,
                content_object=instance,
                description=f"Creat enviament {instance.num_envio}",
                new_value={
                    "num_envio": instance.num_envio,
                    "tipo_respuesta": instance.tipo_respuesta,
                    "fecha_recepcion": instance.fecha_recepcion.isoformat(),
                },
                severity="INFO",
            )
            logger.info(f"Auditat creació d'enviament {instance.num_envio}")
        except Exception as e:
            logger.error(f"Error auditant enviament: {str(e)}", exc_info=True)


@receiver(pre_save, sender=Envio)
def audit_envio_status_change(sender, instance, **kwargs):
    """Auditar canvis d'estat en enviaments"""
    if instance.pk:  # Només si és una actualització
        try:
            old_instance = Envio.objects.get(pk=instance.pk)

            # Detectar canvis importants
            if old_instance.procesado != instance.procesado:
                AuditLog.objects.create(
                    action="UPDATE",
                    user=instance.usuario_envio,
                    content_object=instance,
                    description=f"Canviat estat processament de {instance.num_envio}",
                    old_value={"procesado": old_instance.procesado},
                    new_value={"procesado": instance.procesado},
                    severity="INFO",
                )

            if old_instance.validado != instance.validado:
                AuditLog.objects.create(
                    action="UPDATE",
                    user=instance.usuario_envio,
                    content_object=instance,
                    description=f"Canviat estat validació de {instance.num_envio}",
                    old_value={"validado": old_instance.validado},
                    new_value={"validado": instance.validado},
                    severity="WARNING" if not instance.validado else "INFO",
                )
        except Envio.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error auditant canvi d'estat: {str(e)}", exc_info=True)


@receiver(user_logged_in)
def audit_user_login(sender, request, user, **kwargs):
    """Auditar login exitós"""
    try:
        ip_address = request.META.get("REMOTE_ADDR")

        # Actualitzar última IP de login i restablir comptador d'intents fallits
        # Hem d'actualitzar l'usuari abans de crear el log 'LOGIN' perquè
        # el post_save d'APIUser també genera un AuditLog 'UPDATE' i volem
        # que el log 'LOGIN' sigui el més recent (segons tests).
        try:
            if hasattr(user, "record_successful_login"):
                user.record_successful_login(ip_address=ip_address)
            else:
                # Fallback mínim si el model no exposa el mètode
                if hasattr(user, "last_login_ip"):
                    user.last_login_ip = ip_address
                    user.failed_login_attempts = 0
                    user.account_locked_until = None
                    user.save(update_fields=["last_login_ip", "failed_login_attempts", "account_locked_until"])
        except Exception:
            # No fem fallar l'auditoria per un error no crític en el model d'usuari
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
            user = APIUser.objects.get(username=username)
            # Utilitzar la funció proporcionada pel model
            if hasattr(user, "record_failed_login"):
                user.record_failed_login()
            else:
                # Fallback senzill
                user.failed_login_attempts = getattr(user, "failed_login_attempts", 0) + 1
                user.save(update_fields=["failed_login_attempts"])
        except APIUser.DoesNotExist:
            pass

        logger.warning(f"Intent de login fallit: {username} des de {ip_address}")
    except Exception as e:
        logger.error(f"Error auditant login fallit: {str(e)}", exc_info=True)


@receiver(post_save, sender=APIUser)
def audit_user_changes(sender, instance, created, **kwargs):
    """Auditar canvis en usuaris"""
    try:
        if created:
            AuditLog.objects.create(
                action="CREATE",
                content_object=instance,
                description=f"Creat usuari {instance.username} ({instance.organization})",
                new_value={
                    "username": instance.username,
                    "organization": instance.organization,
                    "cif_organization": instance.cif_organization,
                },
                severity="INFO",
            )
        else:
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
