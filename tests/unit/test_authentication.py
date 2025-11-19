"""
Tests unitaris per autenticació JWT
"""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.unit
@pytest.mark.usefixtures("disable_rate_limiting")
class TestJWTAuthentication:
    """Test suite per autenticació JWT"""

    def test_obtain_token_success(self, api_client, test_user):
        """Test: Obtenir token amb credencials vàlides"""
        url = reverse("authentication:token_obtain_pair")
        data = {"username": "testuser", "password": "TestPassword123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_invalid_credentials(self, api_client, test_user):
        """Test: Token amb credencials invàlides"""
        url = reverse("authentication:token_obtain_pair")
        data = {"username": "testuser", "password": "WrongPassword"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_success(self, api_client, test_user):
        """Test: Refrescar token vàlid"""
        # Primer obtenim tokens
        url_obtain = reverse("authentication:token_obtain_pair")
        data_obtain = {"username": "testuser", "password": "TestPassword123!"}
        response_obtain = api_client.post(url_obtain, data_obtain, format="json")
        refresh_token = response_obtain.data["refresh"]

        # Ara refresquem
        url_refresh = reverse("authentication:token_refresh")
        data_refresh = {"refresh": refresh_token}
        response = api_client.post(url_refresh, data_refresh, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_verify_token_success(self, api_client, test_user):
        """Test: Verificar token vàlid"""
        # Obtenir token
        url_obtain = reverse("authentication:token_obtain_pair")
        data_obtain = {"username": "testuser", "password": "TestPassword123!"}
        response_obtain = api_client.post(url_obtain, data_obtain, format="json")
        access_token = response_obtain.data["access"]

        # Verificar token
        url_verify = reverse("authentication:token_verify")
        data_verify = {"token": access_token}
        response = api_client.post(url_verify, data_verify, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_access_protected_endpoint_without_token(self, api_client):
        """Test: Accedir a endpoint protegit sense token"""
        # Assumint que tens un endpoint /api/sales-notes/
        url = "/api/sales-notes/"

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint_with_valid_token(self, authenticated_client):
        """Test: Accedir a endpoint protegit amb token vàlid"""
        url = "/api/sales-notes/"

        response = authenticated_client.get(url)

        # Pot ser 200 OK o 404 si no hi ha dades encara
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
