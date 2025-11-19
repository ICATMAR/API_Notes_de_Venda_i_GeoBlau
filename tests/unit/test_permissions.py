"""
Tests unitaris per permisos de diferents tipus d'usuaris
"""

import pytest
from rest_framework import status


@pytest.mark.unit
class TestUserPermissions:
    """Test suite per permisos segons tipus d'usuari"""

    def test_darp_can_create_envio(self, darp_client, sample_sales_note_data):
        """Test: DARP pot crear enviaments"""
        url = "/api/sales-notes/envios/"

        response = darp_client.post(url, sample_sales_note_data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            print("\n" + "=" * 80)
            print("ERROR EN CREACIÓ D'ENVIO:")
            print("=" * 80)
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {response.data}")
            print("=" * 80 + "\n")

        assert response.status_code == status.HTTP_201_CREATED
        assert "num_envio" in response.data

    def test_investigador_cannot_create_envio(self, investigador_client, sample_sales_note_data):
        """Test: Investigador NO pot crear enviaments"""
        url = "/api/sales-notes/envios/"

        response = investigador_client.post(url, sample_sales_note_data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_darp_can_list_own_envios(self, darp_client, multiple_envios):
        """Test: DARP pot llistar només els seus enviaments"""
        url = "/api/sales-notes/envios/"

        response = darp_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Només hauria de veure els 2 enviaments del DARP
        assert len(response.data) == 2

    def test_investigador_can_list_all_envios(self, investigador_client, multiple_envios):
        """Test: Investigador pot veure TOTS els enviaments"""
        url = "/api/sales-notes/envios/"

        response = investigador_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Hauria de veure els 3 enviaments (2 DARP + 1 other)
        assert len(response.data) == 3

    def test_admin_can_list_all_envios(self, authenticated_admin_client, multiple_envios):
        """Test: Admin pot veure TOTS els enviaments"""
        url = "/api/sales-notes/envios/"

        response = authenticated_admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Hauria de veure els 3 enviaments
        assert len(response.data) == 3

    def test_darp_can_retrieve_own_envio(self, darp_client, multiple_envios):
        """Test: DARP pot veure detall dels seus enviaments"""
        envio = multiple_envios["darp_envios"][0]
        url = f"/api/sales-notes/envios/{envio.id}/"

        response = darp_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["num_envio"] == envio.num_envio

    def test_darp_cannot_retrieve_other_envio(self, darp_client, multiple_envios):
        """Test: DARP NO pot veure enviaments d'altres usuaris"""
        envio = multiple_envios["other_envios"][0]
        url = f"/api/sales-notes/envios/{envio.id}/"

        response = darp_client.get(url)

        # Hauria de retornar 404 (no troba l'enviament perquè està filtrat)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_investigador_can_retrieve_any_envio(self, investigador_client, multiple_envios):
        """Test: Investigador pot veure detall de qualsevol enviament"""
        # Provar amb enviament del DARP
        darp_envio = multiple_envios["darp_envios"][0]
        url = f"/api/sales-notes/envios/{darp_envio.id}/"

        response = investigador_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["num_envio"] == darp_envio.num_envio

        # Provar amb enviament d'altres
        other_envio = multiple_envios["other_envios"][0]
        url = f"/api/sales-notes/envios/{other_envio.id}/"

        response = investigador_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["num_envio"] == other_envio.num_envio

    def test_unauthenticated_cannot_access(self, api_client):
        """Test: Usuaris no autenticats NO poden accedir"""
        url = "/api/sales-notes/envios/"

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
