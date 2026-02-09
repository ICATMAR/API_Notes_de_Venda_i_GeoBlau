"""
Tests bàsics per a les tasques Celery
"""

import pytest

from sales_notes.tasks import generate_daily_report, process_pending_envios


@pytest.mark.django_db
class TestTasks:
    """Tests per tasques periòdiques"""

    def test_generate_daily_report_executes(self, darp_user):
        """Test que generate_daily_report s'executa sense errors"""
        from sales_notes.models import Envio

        # Crear un enviament de prova
        Envio.objects.create(num_envio="REPORT001", tipo_respuesta=1, usuario_envio=darp_user)

        # Executar la tasca
        result = generate_daily_report()

        # Verificar que retorna l'estructura esperada
        assert isinstance(result, dict)
        assert "date" in result
        assert "total_envios" in result
        assert "by_tipo_respuesta" in result

    def test_process_pending_envios_executes(self, darp_user):
        """Test que process_pending_envios s'executa sense errors"""
        from sales_notes.models import Envio

        # Crear enviaments pendents
        Envio.objects.create(
            num_envio="PEND001", tipo_respuesta=1, usuario_envio=darp_user, procesado=False, validado=False
        )

        # Executar la tasca
        result = process_pending_envios()

        # Verificar que retorna l'estructura esperada
        assert isinstance(result, dict)
        assert "processed" in result
        assert result["processed"] >= 0
