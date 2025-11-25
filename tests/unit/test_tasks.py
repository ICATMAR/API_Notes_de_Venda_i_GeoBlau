"""
Tests per a les tasques periòdiques (Celery tasks)
"""
from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.utils import timezone

from sales_notes.tasks import generate_daily_report, process_pending_envios


@pytest.mark.django_db
class TestGenerateDailyReport:
    """Tests per a la tasca generate_daily_report"""

    def test_generate_daily_report_no_envios(self):
        """Test que genera report sense enviaments"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            # Simular que no hi ha enviaments
            mock_filter = Mock()
            mock_filter.count.return_value = 0
            mock_envio_objects.filter.return_value = mock_filter

            result = generate_daily_report()

        assert result is not None
        assert "date" in result
        assert "total_envios" in result
        assert result["total_envios"] == 0
        assert "by_tipo_respuesta" in result
        assert result["by_tipo_respuesta"][1] == 0
        assert result["by_tipo_respuesta"][2] == 0
        assert result["by_tipo_respuesta"][3] == 0

    def test_generate_daily_report_with_envios(self):
        """Test que genera report amb enviaments"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            # Simular diferents counts per cada tipus
            def filter_side_effect(*args, **kwargs):
                mock_filter = Mock()
                # Total envios
                if "tipo_respuesta" not in kwargs:
                    mock_filter.count.return_value = 15
                # Per tipus
                elif kwargs.get("tipo_respuesta") == 1:
                    mock_filter.count.return_value = 5
                elif kwargs.get("tipo_respuesta") == 2:
                    mock_filter.count.return_value = 7
                elif kwargs.get("tipo_respuesta") == 3:
                    mock_filter.count.return_value = 3
                else:
                    mock_filter.count.return_value = 0
                return mock_filter

            mock_envio_objects.filter.side_effect = filter_side_effect

            with patch("sales_notes.tasks.logger") as mock_logger:
                result = generate_daily_report()

                # Verificar que es fa log de les estadístiques
                mock_logger.info.assert_called_once()

        assert result["total_envios"] == 15
        assert result["by_tipo_respuesta"][1] == 5
        assert result["by_tipo_respuesta"][2] == 7
        assert result["by_tipo_respuesta"][3] == 3

    def test_generate_daily_report_date_range(self):
        """Test que verifica el rang de dates utilitzat"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            with patch("sales_notes.tasks.timezone") as mock_timezone:
                # Simular una data específica
                now = timezone.datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
                yesterday = now - timedelta(days=1)
                mock_timezone.now.return_value = now

                mock_filter = Mock()
                mock_filter.count.return_value = 0
                mock_envio_objects.filter.return_value = mock_filter

                result = generate_daily_report()

                # Verificar que es crida filter amb les dates correctes
                assert mock_envio_objects.filter.called
                # Verificar que la data al result és la d'ahir
                assert "2024-01-14" in result["date"]

    def test_generate_daily_report_returns_dict(self):
        """Test que verifica que retorna un diccionari amb l'estructura esperada"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            mock_filter = Mock()
            mock_filter.count.return_value = 0
            mock_envio_objects.filter.return_value = mock_filter

            result = generate_daily_report()

        assert isinstance(result, dict)
        assert set(result.keys()) == {"date", "total_envios", "by_tipo_respuesta"}
        assert isinstance(result["by_tipo_respuesta"], dict)
        assert set(result["by_tipo_respuesta"].keys()) == {1, 2, 3}


@pytest.mark.django_db
class TestProcessPendingEnvios:
    """Tests per a la tasca process_pending_envios"""

    def test_process_pending_envios_no_pending(self):
        """Test quan no hi ha enviaments pendents"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            # Simular que no hi ha enviaments pendents
            mock_filter = Mock()
            mock_filter.__getitem__ = Mock(return_value=[])
            mock_envio_objects.filter.return_value = mock_filter

            with patch("sales_notes.tasks.logger") as mock_logger:
                result = process_pending_envios()

                # Verificar que es fa log
                mock_logger.info.assert_called_once()
                assert "0" in str(mock_logger.info.call_args)

        assert result["processed"] == 0

    def test_process_pending_envios_with_pending(self):
        """Test amb enviaments pendents"""
        # Crear mocks d'enviaments
        mock_envio1 = Mock()
        mock_envio1.procesado = False
        mock_envio1.save = Mock()

        mock_envio2 = Mock()
        mock_envio2.procesado = False
        mock_envio2.save = Mock()

        mock_envio3 = Mock()
        mock_envio3.procesado = False
        mock_envio3.save = Mock()

        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            # Simular que hi ha 3 enviaments pendents
            mock_filter = Mock()
            mock_filter.__getitem__ = Mock(return_value=[mock_envio1, mock_envio2, mock_envio3])
            mock_envio_objects.filter.return_value = mock_filter

            with patch("sales_notes.tasks.logger") as mock_logger:
                result = process_pending_envios()

                # Verificar que es fa log
                mock_logger.info.assert_called_once()
                assert "3" in str(mock_logger.info.call_args)

        assert result["processed"] == 3

        # Verificar que s'ha actualitzat cada enviament
        assert mock_envio1.procesado is True
        assert mock_envio2.procesado is True
        assert mock_envio3.procesado is True

        mock_envio1.save.assert_called_once_with(update_fields=["procesado"])
        mock_envio2.save.assert_called_once_with(update_fields=["procesado"])
        mock_envio3.save.assert_called_once_with(update_fields=["procesado"])

    def test_process_pending_envios_max_batch_size(self):
        """Test que verifica que només processa màxim 100 enviaments"""
        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            mock_filter = Mock()

            def getitem_side_effect(key):
                # Verificar que es demana slice amb màxim 100
                assert key.stop == 100
                return []

            mock_filter.__getitem__ = Mock(side_effect=getitem_side_effect)
            mock_envio_objects.filter.return_value = mock_filter

            process_pending_envios()

            # Verificar que es filtra per procesado=False i validado=False
            call_kwargs = mock_envio_objects.filter.call_args[1]
            assert call_kwargs["procesado"] is False
            assert call_kwargs["validado"] is False

    def test_process_pending_envios_returns_count(self):
        """Test que verifica que retorna el nombre d'enviaments processats"""
        mock_envio1 = Mock()
        mock_envio1.procesado = False
        mock_envio1.save = Mock()

        mock_envio2 = Mock()
        mock_envio2.procesado = False
        mock_envio2.save = Mock()

        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            mock_filter = Mock()
            mock_filter.__getitem__ = Mock(return_value=[mock_envio1, mock_envio2])
            mock_envio_objects.filter.return_value = mock_filter

            result = process_pending_envios()

        assert isinstance(result, dict)
        assert "processed" in result
        assert result["processed"] == 2

    def test_process_pending_envios_updates_only_procesado_field(self):
        """Test que només actualitza el camp procesado"""
        mock_envio = Mock()
        mock_envio.procesado = False
        mock_envio.validado = False
        mock_envio.save = Mock()

        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            mock_filter = Mock()
            mock_filter.__getitem__ = Mock(return_value=[mock_envio])
            mock_envio_objects.filter.return_value = mock_filter

            process_pending_envios()

        # Verificar que només s'actualitza procesado
        mock_envio.save.assert_called_once_with(update_fields=["procesado"])
        assert mock_envio.procesado is True
        # validado no ha de canviar
        assert mock_envio.validado is False

    def test_process_pending_envios_with_many_pending(self):
        """Test amb molts enviaments pendents (simular 150)"""
        # Crear 150 mocks d'enviaments
        mock_envios = []
        for i in range(150):
            mock_envio = Mock()
            mock_envio.procesado = False
            mock_envio.save = Mock()
            mock_envios.append(mock_envio)

        with patch("sales_notes.tasks.Envio.objects") as mock_envio_objects:
            mock_filter = Mock()
            # Només retornar els primers 100 (comportament del slice [:100])
            mock_filter.__getitem__ = Mock(return_value=mock_envios[:100])
            mock_envio_objects.filter.return_value = mock_filter

            result = process_pending_envios()

        # Només ha de processar 100
        assert result["processed"] == 100
