"""
Models per a la gestió de Notes de Venda (VCPE).
Implementa un patró de 'Staging Layer' per a la ingesta de dades crues.
"""

import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Model abstracte amb timestamps per auditoria"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Envio(TimeStampedModel):
    """
    Model que representa un enviament (batch) de notes de venda.
    Actua com a contenidor per a les dades crues rebudes.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_envio = models.CharField(max_length=50, unique=True, db_index=True, help_text="Número únic d'enviament")
    fecha_recepcion = models.DateTimeField(default=timezone.now, db_index=True)

    # IP i usuari per auditoria
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    usuario_envio = models.ForeignKey("authentication.User", on_delete=models.PROTECT, related_name="envios")

    # Estat del processament que es farà a la base de dades (fora de l'API)
    procesado_en_db = models.BooleanField(
        default=False, db_index=True, help_text="Indica si la BBDD ha processat aquest enviament"
    )
    fecha_procesado_en_db = models.DateTimeField(null=True, blank=True)
    error_procesado = models.TextField(blank=True, null=True, help_text="Error retornat pel procés de la BBDD")

    class Meta:
        db_table = "envio_staging"  # Nom nou per no xocar amb taules existents
        ordering = ["-fecha_recepcion"]
        verbose_name = "Enviament (Staging)"
        verbose_name_plural = "Enviaments (Staging)"

    def __str__(self):
        return f"Envio {self.num_envio} - {self.fecha_recepcion}"


class RawSalesNote(TimeStampedModel):
    """
    Model per guardar el JSON cru de cada nota de venda rebuda.
    Aquesta és la taula de 'staging' principal.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="raw_notes")
    raw_data = models.JSONField(help_text="El payload JSON complet de la nota de venda")

    class Meta:
        db_table = "raw_sales_note"
        ordering = ["-created_at"]
        verbose_name = "Nota de Venda Crua (Staging)"
        verbose_name_plural = "Notes de Venda Crues (Staging)"
