# sales_notes/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from sales_notes.models import Envio, Buque

@pytest.mark.django_db
class TestEnvioModel:
    def test_create_envio_valid(self, api_user):
        """Test creació d'enviament vàlid"""
        envio = Envio.objects.create(
            num_envio="TEST001",
            tipo_respuesta=1,
            usuario_envio=api_user
        )
        assert envio.num_envio == "TEST001"
        assert envio.procesado == False
    
    def test_num_envio_unique(self, api_user):
        """Test constraint d'unicitat"""
        Envio.objects.create(num_envio="TEST001", tipo_respuesta=1, usuario_envio=api_user)
        
        with pytest.raises(Exception):  # IntegrityError
            Envio.objects.create(num_envio="TEST001", tipo_respuesta=1, usuario_envio=api_user)

# sales_notes/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestEnvioAPI:
    def test_create_envio_authenticated(self, api_client, auth_token, sample_envio_data):
        """Test POST amb autenticació vàlida"""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
        response = api_client.post('/api/envios/', sample_envio_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'num_envio' in response.data
    
    def test_create_envio_unauthenticated(self, api_client, sample_envio_data):
        """Test POST sense autenticació rebutjat"""
        response = api_client.post('/api/envios/', sample_envio_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_rate_limiting(self, api_client, auth_token, sample_envio_data):
        """Test rate limiting (100 requests/hora)"""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
        
        # Simular 101 requests
        for i in range(101):
            response = api_client.post('/api/envios/', {**sample_envio_data, 'num_envio': f'TEST{i}'}, format='json')
        
        # L'última hauria de fallar
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

# sales_notes/tests/test_security.py
import pytest

class TestOWASPCompliance:
    def test_sql_injection_protection(self, api_client, auth_token):
        """Test protecció SQL injection"""
        malicious_input = "'; DROP TABLE envio; --"
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
        
        response = api_client.get(f'/api/envios/?search={malicious_input}')
        # Django ORM protegeix automàticament
        assert response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR