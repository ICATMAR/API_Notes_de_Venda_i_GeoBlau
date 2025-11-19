"""
Fixtures globals per als tests de VCPE API

Aquest fitxer conté fixtures reutilitzables per a tots els tests.
Col·loca'l a: tests/conftest.py
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Client API per fer peticions HTTP
    
    Usage:
        def test_endpoint(api_client):
            response = api_client.get('/api/endpoint/')
            assert response.status_code == 200
    """
    return APIClient()


@pytest.fixture
def test_user(db):
    """
    Usuari de test estàndard
    
    Credencials:
        username: testuser
        password: TestPassword123!
        organization: ICATMAR Test
    """
    user = User.objects.create_user(
        username='testuser',
        email='test@icatmar.cat',
        password='TestPassword123!',
        organization='ICATMAR Test',
        is_active=True
    )
    return user


@pytest.fixture
def test_user_credentials():
    """
    Credencials del test_user (sense crear l'usuari)
    
    Útil per tests d'autenticació
    """
    return {
        'username': 'testuser',
        'password': 'TestPassword123!'
    }


@pytest.fixture
def authenticated_client(api_client, test_user):
    """
    Client API autenticat amb JWT
    
    Ja inclou el header Authorization amb un token vàlid
    
    Usage:
        def test_protected_endpoint(authenticated_client):
            response = authenticated_client.get('/api/protected/')
            assert response.status_code == 200
    """
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def admin_user(db):
    """
    Usuari administrador
    
    Credencials:
        username: admin
        password: AdminPassword123!
        is_superuser: True
        is_staff: True
    """
    user = User.objects.create_superuser(
        username='admin',
        email='admin@icatmar.cat',
        password='AdminPassword123!',
        organization='ICATMAR Admin',
        is_active=True
    )
    return user


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """
    Client API autenticat com a administrador
    
    Usage:
        def test_admin_endpoint(authenticated_admin_client):
            response = authenticated_admin_client.get('/api/admin/users/')
            assert response.status_code == 200
    """
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def multiple_test_users(db):
    """
    Crea múltiples usuaris de test
    
    Returns:
        list: Llista de 5 usuaris de test
        
    Usage:
        def test_with_multiple_users(multiple_test_users):
            assert len(multiple_test_users) == 5
            user1, user2, user3, user4, user5 = multiple_test_users
    """
    users = []
    for i in range(1, 6):
        user = User.objects.create_user(
            username=f'testuser{i}',
            email=f'test{i}@icatmar.cat',
            password=f'TestPassword{i}23!',
            organization=f'ICATMAR Test {i}',
            is_active=True
        )
        users.append(user)
    return users

@pytest.fixture
def invalid_sales_note_data():
    """
    Dades invàlides per testejar validació
    
    Returns:
        dict: Payload amb errors de validació
    """
    return {
        "NumEnvio": "",  # Buit (invàlid)
        "TipoRespuesta": 999,  # Valor fora de rang
        # Falten camps obligatoris
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Permet accés a la base de dades per a tots els tests
    
    Aquest fixture s'executa automàticament (autouse=True)
    per cada test que el necessiti
    """
    pass


@pytest.fixture
def mock_redis(monkeypatch):
    """
    Mock de Redis per tests que no necessitin Redis real
    
    Usage:
        def test_with_mock_redis(mock_redis):
            # Redis està mockat
            pass
    """
    from unittest.mock import MagicMock
    
    mock_cache = MagicMock()
    monkeypatch.setattr('django.core.cache.cache', mock_cache)
    
    return mock_cache


@pytest.fixture
def disable_rate_limiting(settings):
    """
    Desactiva rate limiting per als tests
    
    Usage:
        @pytest.mark.usefixtures('disable_rate_limiting')
        def test_many_requests():
            # Rate limiting desactivat
            pass
    """
    settings.RATELIMIT_ENABLE = False
    return settings


# Markers personalitzats
def pytest_configure(config):
    """
    Configura markers personalitzats per pytest
    
    Usage:
        @pytest.mark.unit
        def test_something():
            pass
            
        @pytest.mark.integration
        def test_integration():
            pass
            
        @pytest.mark.security
        def test_security():
            pass
    """
    config.addinivalue_line(
        "markers", "unit: Tests unitaris"
    )
    config.addinivalue_line(
        "markers", "integration: Tests d'integració"
    )
    config.addinivalue_line(
        "markers", "security: Tests de seguretat"
    )
    config.addinivalue_line(
        "markers", "slow: Tests lents que requereixen molt temps"
    )


@pytest.fixture
def capture_audit_logs(db):
    """
    Captura logs d'auditoria durant un test
    
    Returns:
        callable: Funció per obtenir els logs generats
        
    Usage:
        def test_with_audit(capture_audit_logs, authenticated_client):
            authenticated_client.post('/api/sales-notes/', data={...})
            logs = capture_audit_logs()
            assert len(logs) > 0
    """
    from audit.models import AuditLog
    
    initial_count = AuditLog.objects.count()
    
    def get_new_logs():
        return AuditLog.objects.all()[initial_count:]
    
    return get_new_logs


@pytest.fixture
def capture_security_events(db):
    """
    Captura events de seguretat durant un test
    
    Usage:
        def test_security(capture_security_events, api_client):
            # Fer algo que generi event de seguretat
            events = capture_security_events()
            assert len(events) > 0
    """
    from audit.models import SecurityEvent
    
    initial_count = SecurityEvent.objects.count()
    
    def get_new_events():
        return SecurityEvent.objects.all()[initial_count:]
    
    return get_new_events

@pytest.fixture
def api_user(db):
    """Usuari API bàsic"""
    from authentication.models import APIUser
    
    user = APIUser.objects.create_user(
        username='apiuser',
        password='ApiPassword123!',
        email='apiuser@test.com',
        organization='API Test Org',
        cif_organization='B12345678',
        is_active=True
    )
    return user

@pytest.fixture
def darp_user(db):
    """
    Usuari DARP (Generalitat Catalunya)
    
    Pot:
    - Crear enviaments (POST)
    - Consultar els seus propis enviaments (GET)
    """
    from django.contrib.auth.models import Group
    
    # Crear grup DARP si no existeix
    darp_group, _ = Group.objects.get_or_create(name='DARP')
    
    user = User.objects.create_user(
        username='darp_user',
        email='darp@gencat.cat',
        password='DarpPassword123!',
        organization='DARP - Generalitat de Catalunya',
        is_active=True
    )
    user.groups.add(darp_group)
    return user


@pytest.fixture
def darp_client(darp_user):
    """Client API autenticat com a usuari DARP"""
    from rest_framework.test import APIClient

    client = APIClient() 
    refresh = RefreshToken.for_user(darp_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def investigador_user(db):
    """
    Usuari Investigador (ICATMAR)
    
    Pot:
    - Consultar TOTS els enviaments (GET) - només lectura
    - NO pot crear ni modificar
    """
    from django.contrib.auth.models import Group
    
    # Crear grup Investigadors si no existeix
    inv_group, _ = Group.objects.get_or_create(name='Investigadors')
    
    user = User.objects.create_user(
        username='investigador_user',
        email='investigador@icatmar.cat',
        password='InvPassword123!',
        organization='ICATMAR - Investigació',
        is_active=True
    )
    user.groups.add(inv_group)
    return user


@pytest.fixture
def investigador_client(investigador_user):
    """Client API autenticat com a Investigador"""
    from rest_framework.test import APIClient

    client = APIClient()
    refresh = RefreshToken.for_user(investigador_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def multiple_envios(db, darp_user, test_user):
    """
    Crea múltiples enviaments de diferents usuaris per tests
    
    Returns:
        dict: {
            'darp_envios': [envio1, envio2],  # Enviaments del DARP
            'other_envios': [envio3]          # Enviaments d'altres usuaris
        }
    """
    from sales_notes.models import Envio
    
    # Enviaments del DARP
    darp_envio1 = Envio.objects.create(
        num_envio='DARP_ENV_001',
        tipo_respuesta=1,
        usuario_envio=darp_user,
        ip_origen='192.168.1.10'
    )
    darp_envio2 = Envio.objects.create(
        num_envio='DARP_ENV_002',
        tipo_respuesta=2,
        usuario_envio=darp_user,
        ip_origen='192.168.1.10'
    )
    
    # Enviament d'un altre usuari
    other_envio = Envio.objects.create(
        num_envio='OTHER_ENV_001',
        tipo_respuesta=1,
        usuario_envio=test_user,
        ip_origen='192.168.1.20'
    )
    
    return {
        'darp_envios': [darp_envio1, darp_envio2],
        'other_envios': [other_envio]
    }
    
@pytest.fixture
def test_catalog_data(db):
    """
    Crea dades de catàleg necessàries per als tests
    (Vessel, Port, Species)
    
    Returns:
        dict: {'vessels': [vessel_objs], 'port': port_obj, 'species': species_obj}
    """
    from sales_notes.existing_models import Vessel, Port, Species
    
    # Crear TOTS els vaixells necessaris amb registration_num curt
    vessels = []
    vessel_configs = [
        {'id': 9999, 'code': 'TEST-001', 'reg': 'REG001'},
        {'id': 10000, 'code': 'BOAT-001', 'reg': 'REG002'},
    ]
    
    for config in vessel_configs:
        vessel = Vessel.objects.create(
            id=config['id'],
            code=config['code'],
            name=f"Vessel {config['code']}",
            registration_num=config['reg'], 
            base_port_name='Barcelona'
        )
        vessels.append(vessel)
    
    port = Port.objects.create(
        id=9999,
        name='Barcelona',
        code=8,
        latitude=41.38,
        longitude=2.17
    )
    
    species = Species.objects.create(
        id=9999,
        code_3a='HKE',
        scientific_name='Merluccius merluccius',
        catalan_name='Lluç',
        spanish_name='Merluza',
        english_name='Hake'
    )
    
    return {'vessels': vessels, 'port': port, 'species': species}

@pytest.fixture
def sample_sales_note_data(test_catalog_data):
    """
    Dades d'exemple per crear una nota de venda
    ACTUALITZAT per usar dades de catàleg
    
    Returns:
        dict: Payload JSON vàlid per POST /api/sales-notes/envios/
    """
    return {
        "NumEnvio": "TEST_001",
        "TipoRespuesta": 1,
        "EstablecimientosVenta": {
            "EstablecimientoVenta": [{
                "NumIdentificacionEstablec": "LLOTJA_TEST",
                "NombreEstablecimiento": "Llotja de Test",
                "Ventas": {
                    "VentasUnidadProductiva": [{
                        "DatosUnidadProductiva": {
                            "MetodoProduccion": 1,
                            "CodigoBuque": "BOAT-001",
                            "PuertoAL5": "ESBAR",
                            "FechaRegresoPuerto": "2025-10-22T10:00:00Z"
                        },
                        "Especies": {
                            "Especie": [{
                                "NumDocVenta": "NV_TEST_001",
                                "EspecieAL3": "HKE",
                                "FechaVenta": "2025-10-22T11:00:00Z",
                                "Cantidad": 100.5,
                                "Precio": 350.00,
                                "TipoCifNifVendedor": 1,
                                "NIFVendedor": "12345678A",
                                "NombreVendedor": "Test Pescador",
                                "NIFComprador": "B12345678",
                                "IdTipoNifCifComprador": 1,
                                "NombreComprador": "Test Comprador SA"
                            }]
                        }
                    }]
                }
            }]
        }
    }

@pytest.fixture(autouse=True)
def disable_rate_limiting_globally(settings):
    """Desactiva rate limiting globalment per a TOTS els tests"""
    settings.RATELIMIT_ENABLE = False
    if hasattr(settings, 'REST_FRAMEWORK'):
        settings.REST_FRAMEWORK = settings.REST_FRAMEWORK.copy()
        settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
        settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}
    return settings
    

@pytest.fixture
def enable_rate_limiting(settings, disable_rate_limiting_globally):
    """
    Reactiva rate limiting per a tests específics
    """
    # Reactivar AMBDÓS sistemes de rate limiting
    
    # 1. Django-ratelimit (decoradors @ratelimit)
    settings.RATELIMIT_ENABLE = True
    
    # 2. DRF Throttling (REST_FRAMEWORK settings)
    settings.REST_FRAMEWORK = settings.REST_FRAMEWORK.copy()
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ]
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
        'anon': '5/minute',      # Molt baix per tests
        'user': '10/minute'      # Molt baix per tests
    }
    
    # 3. Netejar cache de throttling
    from django.core.cache import cache
    cache.clear()
    
    # 4. IMPORTANT: Re-instanciar els throttles amb els nous settings
    from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
    AnonRateThrottle.cache = cache
    AnonRateThrottle.rate = '5/minute'
    UserRateThrottle.cache = cache  
    UserRateThrottle.rate = '10/minute'
    
    yield settings
    
    # Cleanup: restaurar cache
    cache.clear()