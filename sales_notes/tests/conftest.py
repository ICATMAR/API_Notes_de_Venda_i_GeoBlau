"""
Fixtures específiques per als tests de sales_notes
"""
import pytest
from datetime import date
from django.contrib.auth import get_user_model
from sales_notes.models import (
    Envio,
    EstablecimientoVenta,
    UnidadProductiva,
    Buque,
    Granja,
    PersonaFisicaJuridica,
    Especie,
    FechaCaptura
)

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Crea un usuari de test"""
    user = User.objects.create_user(
        username='testuser',
        email='test@icatmar.cat',
        password='TestPassword123!',
        organization='ICATMAR Test',
        is_active=True
    )
    return user


@pytest.fixture
def envio_basico(test_user):
    """Crea un enviament bàsic"""
    return Envio.objects.create(
        num_envio='TEST_ENV_001',
        tipo_respuesta=1,
        usuario_envio=test_user
    )


@pytest.fixture
def establecimiento_basico(envio_basico):
    """Crea un establiment bàsic"""
    return EstablecimientoVenta.objects.create(
        envio=envio_basico,
        num_identificacion_establec='EST_TEST_001'
    )


@pytest.fixture
def unidad_buque(establecimiento_basico):
    """Crea una unitat productiva amb vaixell"""
    unidad = UnidadProductiva.objects.create(
        establecimiento=establecimiento_basico,
        metodo_produccion=1,
        tipo_unidad='BUQUE'
    )
    Buque.objects.create(
        unidad_productiva=unidad,
        codigo_buque='TEST-BOAT-001',
        puerto_al5='ESBAR',
        armador='Test Armador',
        capitan='Test Capità'
    )
    return unidad


@pytest.fixture
def unidad_granja(establecimiento_basico):
    """Crea una unitat productiva amb granja"""
    unidad = UnidadProductiva.objects.create(
        establecimiento=establecimiento_basico,
        metodo_produccion=2,
        tipo_unidad='GRANJA'
    )
    Granja.objects.create(
        unidad_productiva=unidad,
        codigo_rega='REGA12345',
        lugar_descarga='Puerto Test',
        fecha_produccion=date(2025, 10, 22)
    )
    return unidad


@pytest.fixture
def unidad_persona(establecimiento_basico):
    """Crea una unitat productiva amb persona"""
    unidad = UnidadProductiva.objects.create(
        establecimiento=establecimiento_basico,
        metodo_produccion=3,
        tipo_unidad='PERSONA'
    )
    PersonaFisicaJuridica.objects.create(
        unidad_productiva=unidad,
        nif_persona='12345678A',
        lugar_descarga='Port Test',
        fecha_descarga=date(2025, 10, 22)
    )
    return unidad


@pytest.fixture
def especie_basica(unidad_buque):
    """Crea una espècie bàsica"""
    return Especie.objects.create(
        unidad_productiva=unidad_buque,
        num_doc_venta='NV_TEST_001',
        especie_al3='HKE',
        fecha_venta=date(2025, 10, 22),
        cantidad=100.5,
        precio=350.00,
        tipo_cif_nif_vendedor=1,
        nif_vendedor='12345678A',
        nombre_vendedor='Test Vendedor',
        nif_comprador='B12345678',
        id_tipo_nif_cif_comprador=1,
        nombre_comprador='Test Comprador'
    )


@pytest.fixture
def fecha_captura_basica(especie_basica):
    """Crea una data de captura bàsica"""
    return FechaCaptura.objects.create(
        especie=especie_basica,
        fecha_captura_ini=date(2025, 10, 1),
        fecha_captura_fin=date(2025, 10, 15)
    )


@pytest.fixture
def envio_completo(test_user):
    """
    Crea un enviament complet amb tota la jerarquia:
    Envio -> Establecimiento -> UnidadProductiva -> Buque + Especie + FechaCaptura
    """
    envio = Envio.objects.create(
        num_envio='ENV_COMPLETO_001',
        tipo_respuesta=1,
        usuario_envio=test_user,
        validado=True
    )

    establecimiento = EstablecimientoVenta.objects.create(
        envio=envio,
        num_identificacion_establec='EST_COMPLETO_001'
    )

    unidad = UnidadProductiva.objects.create(
        establecimiento=establecimiento,
        metodo_produccion=1,
        tipo_unidad='BUQUE'
    )

    Buque.objects.create(
        unidad_productiva=unidad,
        codigo_buque='COMPLETO-001',
        puerto_al5='ESBAR',
        armador='Armador Completo',
        capitan='Capità Completo'
    )

    especie1 = Especie.objects.create(
        unidad_productiva=unidad,
        num_doc_venta='NV_COMP_001',
        especie_al3='HKE',
        fecha_venta=date(2025, 10, 22),
        cantidad=100.0,
        precio=350.00,
        tipo_cif_nif_vendedor=1,
        nif_vendedor='12345678A',
        nombre_vendedor='Vendedor 1',
        nif_comprador='B12345678',
        id_tipo_nif_cif_comprador=1,
        nombre_comprador='Comprador 1'
    )

    FechaCaptura.objects.create(
        especie=especie1,
        fecha_captura_ini=date(2025, 10, 1),
        fecha_captura_fin=date(2025, 10, 15)
    )

    especie2 = Especie.objects.create(
        unidad_productiva=unidad,
        num_doc_venta='NV_COMP_002',
        especie_al3='COD',
        fecha_venta=date(2025, 10, 22),
        cantidad=50.0,
        precio=450.00,
        tipo_cif_nif_vendedor=1,
        nif_vendedor='12345678A',
        nombre_vendedor='Vendedor 1',
        nif_comprador='B87654321',
        id_tipo_nif_cif_comprador=1,
        nombre_comprador='Comprador 2'
    )

    return envio


@pytest.fixture
def datos_especie_valida():
    """Diccionari amb dades vàlides per crear una espècie"""
    return {
        'num_doc_venta': 'NV_FIXTURE_001',
        'especie_al3': 'HKE',
        'fecha_venta': '2025-10-22',
        'cantidad': 100.0,
        'precio': 350.00,
        'tipo_cif_nif_vendedor': 1,
        'nif_vendedor': '12345678A',
        'nombre_vendedor': 'Test Vendedor',
        'nif_comprador': 'B12345678',
        'id_tipo_nif_cif_comprador': 1,
        'nombre_comprador': 'Test Comprador'
    }


@pytest.fixture
def datos_buque_valido():
    """Diccionari amb dades vàlides per crear un vaixell"""
    return {
        'codigo_buque': 'FIXTURE-BOAT-001',
        'puerto_al5': 'ESBAR',
        'armador': 'Armador Fixture',
        'capitan': 'Capità Fixture',
        'fecha_regreso_puerto': '2025-10-22T10:00:00Z',
        'cod_marea': 'MAR_FIXTURE_001'
    }


@pytest.fixture
def datos_granja_valida():
    """Diccionari amb dades vàlides per crear una granja"""
    return {
        'codigo_rega': 'REGA_FIXTURE',
        'lugar_descarga': 'Puerto Fixture',
        'fecha_produccion': '2025-10-22'
    }


@pytest.fixture
def datos_persona_valida():
    """Diccionari amb dades vàlides per crear una persona"""
    return {
        'nif_persona': '87654321B',
        'lugar_descarga': 'Port Fixture',
        'fecha_descarga': '2025-10-22'
    }
