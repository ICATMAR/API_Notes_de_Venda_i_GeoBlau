"""
Tests addicionals per cobrir sales_notes/views.py
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestEnvioViewSetCoverage:
    """Tests per cobrir línies accessibles de EnvioViewSet"""

    def test_envio_status_endpoint(self, darp_client, darp_user):
        """Test endpoint /envios/{id}/status/ (línia 178-183, 92)"""
        from sales_notes.models import Envio

        # Crear un enviament
        envio = Envio.objects.create(
            num_envio="STATUS_TEST", tipo_respuesta=1, usuario_envio=darp_user, procesado=True, validado=True
        )

        url = f"/api/sales-notes/envios/{envio.id}/status/"
        response = darp_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "procesado" in response.data
        assert response.data["procesado"] is True

    def test_list_uses_list_serializer(self, darp_client, darp_user):
        """Test que list usa EnvioListSerializer (línia 90)"""
        from sales_notes.models import Envio

        Envio.objects.create(num_envio="LIST_TEST", tipo_respuesta=1, usuario_envio=darp_user)

        url = "/api/sales-notes/envios/"
        response = darp_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_retrieve_envio_detail(self, darp_client, darp_user):
        """Test retrieve amb logging (línia 161)"""
        from sales_notes.models import Envio

        envio = Envio.objects.create(num_envio="RETRIEVE_TEST", tipo_respuesta=1, usuario_envio=darp_user)

        url = f"/api/sales-notes/envios/{envio.id}/"
        response = darp_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["num_envio"] == "RETRIEVE_TEST"


@pytest.mark.django_db
class TestSerializersValidation:
    """Tests per cobrir validacions de serializers"""

    def test_envio_serializer_with_invalid_tipo_respuesta(self, darp_user):
        """Test validació de tipo_respuesta"""
        from sales_notes.serializers import EnvioSerializer

        data = {"num_envio": "TEST_INVALID", "tipo_respuesta": 999, "usuario_envio": darp_user.id}  # Valor invàlid

        serializer = EnvioSerializer(data=data)
        assert not serializer.is_valid()

    def test_buque_serializer_validation(self):
        """Test validacions de BuqueSerializer"""
        from sales_notes.serializers import BuqueSerializer

        # Test amb dades invàlides
        data = {
            "codigo_buque": "",  # Buit
        }

        serializer = BuqueSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestModelsEdgeCases:
    """Tests per cobrir casos edge dels models"""

    def test_envio_str_representation(self, darp_user):
        """Test __str__ del model Envio"""
        from sales_notes.models import Envio

        envio = Envio.objects.create(num_envio="STR_TEST", tipo_respuesta=1, usuario_envio=darp_user)

        str_repr = str(envio)
        assert "STR_TEST" in str_repr


@pytest.mark.django_db
class TestPermissionsEdgeCases:
    """Tests per cobrir casos dels permisos"""

    def test_admin_has_full_access(self, authenticated_admin_client, admin_user):
        """Test que admin té accés complet (línia 73-74 views.py)"""
        url = "/api/sales-notes/envios/"
        response = authenticated_admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_investigador_can_see_all(self, investigador_client, darp_user, test_user):
        """Test que investigador veu tots els enviaments (línia 77-78 views.py)"""
        from sales_notes.models import Envio

        # Crear enviaments de diferents usuaris
        Envio.objects.create(num_envio="INV_TEST_1", tipo_respuesta=1, usuario_envio=darp_user)
        Envio.objects.create(num_envio="INV_TEST_2", tipo_respuesta=1, usuario_envio=test_user)

        url = "/api/sales-notes/envios/"
        response = investigador_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Hauria de veure tots els enviaments
        assert len(response.data) >= 2
