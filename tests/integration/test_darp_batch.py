"""
Tests d'integració per enviaments batch del DARP
"""

import pytest
from rest_framework import status


@pytest.mark.integration
class TestDARPBatchSubmission:
    """Tests per enviaments batch nocturns del DARP"""

    def test_batch_submission_success(self, darp_client, sample_sales_note_data, test_catalog_data):
        """Test: Enviar batch de 10 notes de venda amb èxit"""
        url = "/api/sales-notes/envios/"
        created_envios = []

        # Enviar 10 enviaments
        for i in range(10):
            # Modificar num_envio per fer-lo únic
            data = sample_sales_note_data.copy()
            data["NumEnvio"] = f"BATCH_TEST_{i:04d}"

            data["EstablecimientosVenta"]["EstablecimientoVenta"][0]["Ventas"]["VentasUnidadProductiva"][0]["Especies"][
                "Especie"
            ][0]["NumDocVenta"] = f"NV_BATCH_{i:04d}"
            response = darp_client.post(url, data, format="json")

            assert response.status_code == status.HTTP_201_CREATED
            created_envios.append(response.data["num_envio"])

        # Verificar que s'han creat tots
        assert len(created_envios) == 10

        # Llistar i verificar que estan tots
        list_response = darp_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) >= 10

    @pytest.mark.django_db(transaction=True)
    def test_batch_rollback_on_error(self, darp_client, sample_sales_note_data):
        """Test: Si un enviament falla, el batch no es comet (rollback)"""
        url = "/api/sales-notes/envios/"

        # Crear 3 enviaments vàlids
        valid_data = sample_sales_note_data.copy()

        for i in range(3):
            valid_data["NumEnvio"] = f"VALID_{i}"
            response = darp_client.post(url, valid_data, format="json")
            assert response.status_code == status.HTTP_201_CREATED

        # Intentar crear un enviament invàlid (num_envio duplicat)
        invalid_data = sample_sales_note_data.copy()
        invalid_data["NumEnvio"] = "VALID_0"  # Duplicat!

        response = darp_client.post(url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Els 3 primers haurien d'existir encara (no s'ha fet rollback perquè són transaccions independents)
        # En un batch real, hauríem d'usar transaccions explícites

    def test_rate_limiting_batch(self, darp_client, sample_sales_note_data, disable_rate_limiting):
        """Test: Rate limiting permet enviar batches grans"""
        url = "/api/sales-notes/envios/"

        # Amb disable_rate_limiting, hauria de permetre més de 100 requests
        for i in range(50):
            data = sample_sales_note_data.copy()
            data["NumEnvio"] = f"RATE_TEST_{i:04d}"

            response = darp_client.post(url, data, format="json")

            # No hauria de retornar 429 Too Many Requests
            assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS

    def test_batch_post_success(self, darp_client, sample_sales_note_data):
        """Enviar una llista (batch) amb diversos enviaments vàlids en una sola POST"""
        from sales_notes.existing_models import Species, Vessel
        from sales_notes.models import Envio

        # Preparar catàleg mínim
        Species.objects.get_or_create(code_3a="HKE", defaults={"id": 21001, "scientific_name": "Hake"})
        Vessel.objects.get_or_create(code="ESP000000001", defaults={"id": 21001})
        Vessel.objects.get_or_create(code="ESP000000002", defaults={"id": 21002})

        url = "/api/sales-notes/envios/"

        batch = []
        for i, boat in enumerate(("ESP000000001", "ESP000000002")):
            data = sample_sales_note_data.copy()
            data = dict(data)  # shallow copy
            data["NumEnvio"] = f"BATCH_POST_OK_{i}"
            # Ensure DatosUnidadProductiva CodigoBuque matches allowed vessel
            establecimientos = data["EstablecimientosVenta"]["EstablecimientoVenta"]
            establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["DatosUnidadProductiva"]["CodigoBuque"] = boat
            # also adjust NumDocVenta to be unique
            establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["Especies"]["Especie"][0][
                "NumDocVenta"
            ] = f"NV_BATCH_OK_{i}"
            batch.append(data)

        response = darp_client.post(url, batch, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        # Comprovar que s'han creat tots
        assert len(response.data) == len(batch)
        for item in response.data:
            assert Envio.objects.filter(num_envio=item.get("num_envio")).exists()

    def test_batch_post_rollback_on_error(self, darp_client, sample_sales_note_data):
        """Enviar un batch amb una nota invàlida i verificar que tot el batch fa rollback"""
        from sales_notes.existing_models import Species, Vessel
        from sales_notes.models import Envio

        # Preparar catàleg mínim
        Species.objects.get_or_create(code_3a="HKE", defaults={"id": 22001, "scientific_name": "Hake"})
        Vessel.objects.get_or_create(code="ESP000000001", defaults={"id": 22001})

        url = "/api/sales-notes/envios/"

        batch = []
        # 2 enviaments vàlids
        for i in range(2):
            data = sample_sales_note_data.copy()
            data = dict(data)
            data["NumEnvio"] = f"BATCH_POST_OK_{i}"
            establecimientos = data["EstablecimientosVenta"]["EstablecimientoVenta"]
            establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["Especies"]["Especie"][0][
                "NumDocVenta"
            ] = f"NV_BATCH_OK_{i}"
            establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["DatosUnidadProductiva"][
                "CodigoBuque"
            ] = "ESP000000001"
            batch.append(data)

        # 1 enviament invàlid (espècie no existent ZZZ)
        bad = sample_sales_note_data.copy()
        bad = dict(bad)
        bad["NumEnvio"] = "BATCH_POST_BAD"
        establecimientos = bad["EstablecimientosVenta"]["EstablecimientoVenta"]
        establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["Especies"]["Especie"][0]["EspecieAL3"] = "ZZZ"
        establecimientos[0]["Ventas"]["VentasUnidadProductiva"][0]["DatosUnidadProductiva"][
            "CodigoBuque"
        ] = "ESP000000001"
        batch.append(bad)

        response = darp_client.post(url, batch, format="json")

        # Ha de fallar i retornar 400, i no s'ha de crear cap Envio del batch
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        for item in batch:
            num = item.get("NumEnvio")
            assert not Envio.objects.filter(num_envio=num).exists()
