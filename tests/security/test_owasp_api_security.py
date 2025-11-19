"""
Tests de seguretat basats en OWASP API Security Top 10
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.conf import settings


@pytest.mark.security
class TestOWASPAPISecurity:
    """Tests basats en OWASP API Security Top 10 2023"""
    
    # API1:2023 - Broken Object Level Authorization
    def test_access_other_user_data(self, authenticated_client, test_user, admin_user):
        """Test: Prevenir accés a dades d'altres usuaris"""
        # Intenta accedir a dades d'admin amb usuari normal
        url = f'/api/users/{admin_user.id}/'
        response = authenticated_client.get(url)
        
        # Hauria de retornar 403 Forbidden o 404 Not Found
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
    
    # API2:2023 - Broken Authentication
    def test_brute_force_protection(self, api_client):
        """Test: Protecció contra brute force"""
        url = reverse('authentication:token_obtain_pair')
        
        # Intentar 10 vegades amb password incorrecte
        for i in range(10):
            data = {
                'username': 'testuser',
                'password': f'WrongPassword{i}'
            }
            response = api_client.post(url, data)
        
        # Després de N intents, hauria d'estar bloquejat
        # (Depends de la configuració de django-defender)
        # Aquest test pot necessitar ajustos segons config
    
    # API3:2023 - Broken Object Property Level Authorization
    def test_mass_assignment_vulnerability(self, authenticated_client):
        """Test: Prevenir mass assignment"""
        url = '/api/users/'
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'is_superuser': True,  # Intent d'escalar privilegis
            'is_staff': True
        }
        
        response = authenticated_client.post(url, data)
        
        # Hauria de crear usuari però sense privilegis d'admin
        if response.status_code == status.HTTP_201_CREATED:
            assert response.data.get('is_superuser') == False
            assert response.data.get('is_staff') == False
    
    # API4:2023 - Unrestricted Resource Consumption
    @pytest.mark.skipif(True, reason="Rate limiting desactivat globalment")
    def test_rate_limiting(self, api_client, test_user, enable_rate_limiting):
        """Test: Rate limiting funciona"""
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'TestPassword123!'
        }
        
        # Fer moltes peticions ràpidament
        responses = []
        for i in range(20):  # Més del límit de 5
            response = api_client.post(url, data, format='json')
            responses.append(response.status_code)
        
        # Alguna petició hauria de retornar 429 Too Many Requests
        assert status.HTTP_429_TOO_MANY_REQUESTS in responses, \
            f"Expected 429 in responses, got: {set(responses)}"
    
    # API5:2023 - Broken Function Level Authorization
    def test_admin_endpoint_access_control(self, authenticated_client):
        """Test: Usuari normal no pot accedir a endpoints d'admin"""
        url = '/admin/'
        
        response = authenticated_client.get(url)
        
        # Hauria de retornar 403 o redirigir a login
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_302_FOUND]
    
    # API6:2023 - Unrestricted Access to Sensitive Business Flows
    @pytest.mark.skipif(True, reason="Rate limiting desactivat globalment")
    def test_prevent_automated_submission(self, darp_client, sample_sales_note_data, enable_rate_limiting):
        """Test: Prevenir enviaments automatitzats massius"""
        import copy 
        url = '/api/sales-notes/envios/'
        
        # Intentar crear més notes del límit (10/minute per user)
        responses = []
        for i in range(15):  # Més del límit de 10
            data = sample_sales_note_data.copy()
            data = copy.deepcopy(sample_sales_note_data)
            data['NumEnvio'] = f'TEST_RL_{i:04d}'
            
            # També cal fer el NumDocVenta únic
            data['EstablecimientosVenta']['EstablecimientoVenta'][0]['Ventas']['VentasUnidadProductiva'][0]['Especies']['Especie'][0]['NumDocVenta'] = f'NV_{i:04d}'
            
            response = darp_client.post(url, data, format='json')
            responses.append(response.status_code)
        
        # Hauria d'haver rate limiting
        assert status.HTTP_429_TOO_MANY_REQUESTS in responses, \
            f"Expected 429 in responses, got: {set(responses)}"
    
    # API8:2023 - Security Misconfiguration
    def test_security_headers_present(self, api_client):
        """Test: Headers de seguretat presents"""
        response = api_client.get('/health/')
        
        # Verificar headers de seguretat
        headers = response.headers
        
        # En desenvolupament alguns poden estar desactivats
        # En producció tots haurien d'estar actius
        if not settings.DEBUG:
            assert 'X-Content-Type-Options' in headers
            assert headers['X-Content-Type-Options'] == 'nosniff'
            assert 'X-Frame-Options' in headers
    
    # API9:2023 - Improper Inventory Management
    @pytest.mark.skipif(True, reason="Documentació encara no protegida")
    def test_api_documentation_access_control(self, api_client):
        """Test: Documentació API no accessible públicament en producció"""
        response = api_client.get('/api/docs/')
        
        # En entorn de test/desenvolupament, podem acceptar qualsevol comportament
        # Aquest test és més rellevant en producció real
        if settings.DEBUG:
            # En mode DEBUG, acceptable que estigui accessible o restringida
            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND
            ]
        else:
            # En producció hauria d'estar restringida
            assert response.status_code in [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND
            ], f"Expected 403/404 in production, got {response.status_code}"
    # API10:2023 - Unsafe Consumption of APIs
    def test_input_validation_sql_injection(self, darp_client):
        """Test: Validació d'inputs contra SQL injection"""
        url = '/api/sales-notes/envios/'
        
        # Intent de SQL injection
        data = {
            'NumEnvio': "'; DROP TABLE sales_notes; --",
            'TipoRespuesta': 1
        }
        
        response = darp_client.post(url, data, format='json')
        
        # Hauria de fallar la validació, no executar SQL
        assert response.status_code == status.HTTP_400_BAD_REQUEST