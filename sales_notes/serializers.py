"""
Serialitzadors per a l'API de notes de venda (Staging Layer)
"""

import logging

from rest_framework import serializers

from .models import (
    Envio,
)

logger = logging.getLogger(__name__)


class EnvioStagingSerializer(serializers.ModelSerializer):
    """
    Serialitzador per a la ingesta d'enviaments en fase de Staging.
    Accepta el JSON complet, crea l'Envio i genera RawSalesNotes per a cada venda.
    """

    # Camp per rebre el JSON cru complet
    raw_payload = serializers.JSONField(write_only=True)

    class Meta:
        model = Envio
        fields = [
            "id",
            "num_envio",
            "fecha_recepcion",
            "usuario_envio",
            "procesado_en_db",
            "error_procesado",
            "raw_payload",
        ]
        read_only_fields = [
            "id",
            "fecha_recepcion",
            "usuario_envio",
            "procesado_en_db",
            "error_procesado",
        ]

    def to_internal_value(self, data):
        """
        Mapeig manual de camps PascalCase a snake_case per a l'Envio
        i preservació del payload complet.
        """
        internal = {}
        if "NumEnvio" not in data:
            raise serializers.ValidationError({"NumEnvio": "Aquest camp és obligatori."})
        internal["num_envio"] = data["NumEnvio"]

        # Guardem tot el JSON per processar-lo al create()
        internal["raw_payload"] = data
        return internal

    def create(self, validated_data):
        """
        Crea l'Envio.
        La creació de la RawSalesNote amb el JSON complet es gestiona a la vista.
        """
        raw_payload = validated_data.pop("raw_payload")
        user = self.context["request"].user
        ip_address = self.context["request"].META.get("REMOTE_ADDR")

        # 1. Crear l'Envio (Capçalera)
        envio = Envio.objects.create(usuario_envio=user, ip_origen=ip_address, num_envio=raw_payload["NumEnvio"])

        return envio
