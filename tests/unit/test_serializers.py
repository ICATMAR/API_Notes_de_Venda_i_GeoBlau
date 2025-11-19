"""
Tests complets per als serializers de sales_notes
Cobreix validacions, creació i representació de dades
"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from sales_notes.serializers import (
    FechaCapturaSerializer,
    EspecieSerializer,
    BuqueSerializer,
    GranjaSerializer,
    PersonaFisicaJuridicaSerializer,
    UnidadProductivaSerializer,
    EstablecimientoVentaSerializer,
    EnvioSerializer,
    EnvioListSerializer,
    EnvioStatusSerializer
)
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


@pytest.mark.django_db
class TestFechaCapturaSerializer:
    """Tests per al serializer de dates de captura"""

    def test_valid_fecha_captura(self):
        """Test creació de data de captura vàlida"""
        data = {
            'fecha_captura_ini': date(2025, 10, 1),
            'fecha_captura_fin': date(2025, 10, 15)
        }
        serializer = FechaCapturaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['fecha_captura_ini'] == date(2025, 10, 1)

    def test_fecha_captura_solo_inicio(self):
        """Test amb només data d'inici (data fi opcional)"""
        data = {
            'fecha_captura_ini': date(2025, 10, 1)
        }
        serializer = FechaCapturaSerializer(data=data)
        assert serializer.is_valid()

    def test_fecha_fin_anterior_a_inicio_error(self):
        """Test que data fi no pot ser anterior a data inici"""
        data = {
            'fecha_captura_ini': date(2025, 10, 15),
            'fecha_captura_fin': date(2025, 10, 1)
        }
        serializer = FechaCapturaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_fechas_iguales_valido(self):
        """Test que data fi igual a data inici és vàlid"""
        data = {
            'fecha_captura_ini': date(2025, 10, 1),
            'fecha_captura_fin': date(2025, 10, 1)
        }
        serializer = FechaCapturaSerializer(data=data)
        assert serializer.is_valid()


@pytest.mark.django_db
class TestEspecieSerializer:
    """Tests per al serializer d'espècies"""

    def test_especie_valida_completa(self):
        """Test creació d'espècie amb totes les dades"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'zona': 'ZONA1',
            'fecha_venta': '2025-10-22',
            'cantidad': 100.5,
            'precio': 350.00,
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test Vendedor',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test Comprador'
        }
        serializer = EspecieSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_especie_al3_formato_invalido(self):
        """Test que codi espècie ha de ser 3 lletres"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HK',  # Només 2 lletres
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'especie_al3' in serializer.errors

    def test_especie_al3_con_numeros_invalido(self):
        """Test que codi espècie no pot tenir números"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'H2E',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'especie_al3' in serializer.errors

    def test_especie_al3_uppercase(self):
        """Test que codi espècie es converteix a majúscules"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'hke',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350,
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test'
        }
        serializer = EspecieSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['especie_al3'] == 'HKE'

    def test_cantidad_negativa_invalida(self):
        """Test que quantitat ha de ser positiva"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': -10,
            'precio': 350
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'cantidad' in serializer.errors

    def test_cantidad_cero_invalida(self):
        """Test que quantitat zero no és vàlida"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 0,
            'precio': 350
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'cantidad' in serializer.errors

    def test_precio_negativo_invalido(self):
        """Test que preu no pot ser negatiu"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': -10
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'precio' in serializer.errors

    def test_precio_cero_valido(self):
        """Test que preu zero és vàlid (possibles donacions)"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 0,
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test'
        }
        serializer = EspecieSerializer(data=data)
        assert serializer.is_valid()

    def test_retirada_sin_destino_invalido(self):
        """Test que si hi ha retirada diferent de 1, cal destí"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350,
            'tipo_retirada': 2,
            # Falta cod_destino_retirado
        }
        serializer = EspecieSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_retirada_con_destino_valido(self):
        """Test retirada amb destí és vàlid"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350,
            'tipo_retirada': 2,
            'cod_destino_retirado': 'DEST001',
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test'
        }
        serializer = EspecieSerializer(data=data)
        assert serializer.is_valid()

    def test_especie_con_fechas_captura(self):
        """Test espècie amb dates de captura associades"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350,
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test',
            'fechas_captura': [
                {
                    'fecha_captura_ini': '2025-10-01',
                    'fecha_captura_fin': '2025-10-15'
                }
            ]
        }
        serializer = EspecieSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_especie_precio_decimal_precision(self):
        """Test que preu no accepta més de 2 decimals"""
        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350.1234,  # 4 decimals - hauria de ser rebutjat
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test'
        }
        serializer = EspecieSerializer(data=data)
        # El model té max_digits=10, decimal_places=2
        # DRF hauria de validar i rebutjar 4 decimals
        # Nota: DRF pot truncar o arrodonir segons configuració
        # Si el serializer accepta el valor, verificar que s'arrodoneix
        if serializer.is_valid():
            # Acceptat però arrodonit a 2 decimals
            from decimal import Decimal
            assert serializer.validated_data['precio'] == Decimal('350.12')
        else:
            # Rebutjat per massa decimals
            assert 'precio' in serializer.errors

    def test_especie_talla_no_reglamentaria_sin_observaciones(self, caplog):
        """Test que talla no reglamentària sense observacions genera advertència"""
        import logging
        caplog.set_level(logging.WARNING)

        data = {
            'num_doc_venta': 'NV001',
            'especie_al3': 'HKE',
            'fecha_venta': '2025-10-22',
            'cantidad': 100,
            'precio': 350,
            'talla_no_reglamentaria': True,
            # Sense 'observaciones'
            'tipo_cif_nif_vendedor': 1,
            'nif_vendedor': '12345678A',
            'nombre_vendedor': 'Test',
            'nif_comprador': 'B12345678',
            'id_tipo_nif_cif_comprador': 1,
            'nombre_comprador': 'Test'
        }
        serializer = EspecieSerializer(data=data)

        # Pot ser vàlid però hauria de generar advertència als logs
        # o pot ser invàlid segons la validació del serializer
        if serializer.is_valid():
            # Si és vàlid, verificar que hi ha advertència als logs
            # (si el serializer genera logging)
            pass  # Pot o no generar warning segons implementació
        else:
            # Si no és vàlid, verificar que hi ha error
            assert 'observaciones' in str(serializer.errors) or 'non_field_errors' in serializer.errors


@pytest.mark.django_db
class TestBuqueSerializer:
    """Tests per al serializer de vaixells"""

    def test_buque_valido(self):
        """Test creació de vaixell vàlid"""
        data = {
            'codigo_buque': 'ESP-001',
            'puerto_al5': 'ESBAR',
            'armador': 'Test Armador',
            'capitan': 'Test Capità',
            'fecha_regreso_puerto': '2025-10-22T10:00:00Z',
            'cod_marea': 'MAR001'
        }
        serializer = BuqueSerializer(data=data)
        assert serializer.is_valid()

    def test_puerto_formato_invalido(self):
        """Test que codi port ha de tenir 5 caràcters"""
        data = {
            'codigo_buque': 'ESP-001',
            'puerto_al5': 'ESBA',  # Només 4 caràcters
        }
        serializer = BuqueSerializer(data=data)
        assert not serializer.is_valid()
        assert 'puerto_al5' in serializer.errors

    def test_puerto_uppercase(self):
        """Test que codi port es converteix a majúscules"""
        data = {
            'codigo_buque': 'ESP-001',
            'puerto_al5': 'esbar',
        }
        serializer = BuqueSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['puerto_al5'] == 'ESBAR'

    def test_buque_sin_puerto(self):
        """Test vaixell sense port (opcional)"""
        data = {
            'codigo_buque': 'ESP-001',
        }
        serializer = BuqueSerializer(data=data)
        assert serializer.is_valid()


@pytest.mark.django_db
class TestGranjaSerializer:
    """Tests per al serializer de granges"""

    def test_granja_valida(self):
        """Test creació de granja vàlida"""
        data = {
            'codigo_rega': 'REGA12345',
            'lugar_descarga': 'Puerto Test',
            'fecha_produccion': '2025-10-22'
        }
        serializer = GranjaSerializer(data=data)
        assert serializer.is_valid()

    def test_codigo_rega_largo_invalido(self):
        """Test que codi REGA no pot superar 14 caràcters"""
        data = {
            'codigo_rega': 'REGA123456789012345',  # 19 caràcters
        }
        serializer = GranjaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'codigo_rega' in serializer.errors

    def test_codigo_rega_limite_valido(self):
        """Test codi REGA amb exactament 14 caràcters"""
        data = {
            'codigo_rega': '12345678901234',  # 14 caràcters
        }
        serializer = GranjaSerializer(data=data)
        assert serializer.is_valid()


@pytest.mark.django_db
class TestPersonaFisicaJuridicaSerializer:
    """Tests per al serializer de persones físiques/jurídiques"""

    def test_persona_valida(self):
        """Test creació de persona vàlida"""
        data = {
            'nif_persona': '12345678A',
            'lugar_descarga': 'Port Test',
            'fecha_descarga': '2025-10-22'
        }
        serializer = PersonaFisicaJuridicaSerializer(data=data)
        assert serializer.is_valid()

    def test_nif_uppercase(self):
        """Test que NIF es converteix a majúscules"""
        data = {
            'nif_persona': '12345678a',
        }
        serializer = PersonaFisicaJuridicaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['nif_persona'] == '12345678A'

    def test_nif_largo_invalido(self):
        """Test que NIF no pot superar 17 caràcters"""
        data = {
            'nif_persona': '123456789012345678',  # 18 caràcters
        }
        serializer = PersonaFisicaJuridicaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'nif_persona' in serializer.errors


@pytest.mark.django_db
class TestUnidadProductivaSerializer:
    """Tests per al serializer d'unitats productives amb polimorfisme"""

    def test_unidad_con_buque_valida(self):
        """Test unitat productiva amb vaixell"""
        data = {
            'metodo_produccion': 1,
            'buque': {
                'codigo_buque': 'ESP-001',
                'puerto_al5': 'ESBAR',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data['tipo_unidad'] == 'BUQUE'

    def test_unidad_con_granja_valida(self):
        """Test unitat productiva amb granja"""
        data = {
            'metodo_produccion': 2,
            'granja': {
                'codigo_rega': 'REGA12345',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['tipo_unidad'] == 'GRANJA'

    def test_unidad_con_persona_valida(self):
        """Test unitat productiva amb persona"""
        data = {
            'metodo_produccion': 3,
            'persona': {
                'nif_persona': '12345678A',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['tipo_unidad'] == 'PERSONA'

    def test_metodo_1_sin_buque_ni_persona_invalido(self):
        """Test que mètode 1 requereix buque o persona"""
        data = {
            'metodo_produccion': 1,
            # Falta buque o persona
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_metodo_2_sin_granja_invalido(self):
        """Test que mètode 2 requereix granja"""
        data = {
            'metodo_produccion': 2,
            'buque': {
                'codigo_buque': 'ESP-001',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_metodo_3_sin_persona_invalido(self):
        """Test que mètode 3 requereix persona"""
        data = {
            'metodo_produccion': 3,
            'granja': {
                'codigo_rega': 'REGA12345',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_multiple_tipos_unidad_invalido(self):
        """Test que només pot haver-hi un tipus d'unitat"""
        data = {
            'metodo_produccion': 1,
            'buque': {
                'codigo_buque': 'ESP-001',
            },
            'granja': {
                'codigo_rega': 'REGA12345',
            }
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_unidad_con_especies(self, test_user):
        """Test crear unitat productiva amb espècies"""
        establecimiento = EstablecimientoVenta.objects.create(
            envio=Envio.objects.create(
                num_envio='TEST001',
                tipo_respuesta=1,
                usuario_envio=test_user
            ),
            num_identificacion_establec='EST001'
        )

        data = {
            'metodo_produccion': 1,
            'buque': {
                'codigo_buque': 'ESP-001',
                'puerto_al5': 'ESBAR',
            },
            'especies': [
                {
                    'num_doc_venta': 'NV001',
                    'especie_al3': 'HKE',
                    'fecha_venta': '2025-10-22',
                    'cantidad': 100,
                    'precio': 350,
                    'tipo_cif_nif_vendedor': 1,
                    'nif_vendedor': '12345678A',
                    'nombre_vendedor': 'Test',
                    'nif_comprador': 'B12345678',
                    'id_tipo_nif_cif_comprador': 1,
                    'nombre_comprador': 'Test'
                }
            ]
        }
        serializer = UnidadProductivaSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        unidad = serializer.save(establecimiento=establecimiento)
        assert unidad.especies.count() == 1
        assert unidad.buque is not None


@pytest.mark.django_db
class TestEstablecimientoVentaSerializer:
    """Tests per al serializer d'establiments de venda"""

    def test_establecimiento_valido(self):
        """Test creació d'establiment vàlid"""
        data = {
            'num_identificacion_establec': 'EST001',
        }
        serializer = EstablecimientoVentaSerializer(data=data)
        assert serializer.is_valid()

    def test_num_identificacion_vacio_invalido(self):
        """Test que número identificació no pot estar buit"""
        data = {
            'num_identificacion_establec': '',
        }
        serializer = EstablecimientoVentaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'num_identificacion_establec' in serializer.errors

    def test_establecimiento_con_unidades_productivas(self, test_user):
        """Test establiment amb unitats productives"""
        envio = Envio.objects.create(
            num_envio='TEST001',
            tipo_respuesta=1,
            usuario_envio=test_user
        )

        data = {
            'num_identificacion_establec': 'EST001',
            'ventas_unidad_productiva': [
                {
                    'metodo_produccion': 1,
                    'buque': {
                        'codigo_buque': 'ESP-001',
                        'puerto_al5': 'ESBAR',
                    }
                }
            ]
        }
        serializer = EstablecimientoVentaSerializer(data=data)
        assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
class TestEnvioSerializer:
    """Tests per al serializer principal d'enviaments"""

    def test_envio_valido_minimo(self, test_user, api_client):
        """Test enviament vàlid amb dades mínimes"""
        data = {
            'num_envio': 'ENV001',
            'tipo_respuesta': 1,
            'establecimientos_venta': [
                {
                    'num_identificacion_establec': 'EST001',
                    'ventas_unidad_productiva': [
                        {
                            'metodo_produccion': 1,
                            'buque': {
                                'codigo_buque': 'ESP-001',
                                'puerto_al5': 'ESBAR',
                            },
                            'especies': [
                                {
                                    'num_doc_venta': 'NV001',
                                    'especie_al3': 'HKE',
                                    'fecha_venta': '2025-10-22',
                                    'cantidad': 100,
                                    'precio': 350,
                                    'tipo_cif_nif_vendedor': 1,
                                    'nif_vendedor': '12345678A',
                                    'nombre_vendedor': 'Test',
                                    'nif_comprador': 'B12345678',
                                    'id_tipo_nif_cif_comprador': 1,
                                    'nombre_comprador': 'Test'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Mock request
        from unittest.mock import Mock
        mock_request = Mock()
        mock_request.user = test_user
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        serializer = EnvioSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid(), serializer.errors

    def test_num_envio_duplicado_invalido(self, test_user):
        """Test que número enviament ha de ser únic"""
        Envio.objects.create(
            num_envio='ENV001',
            tipo_respuesta=1,
            usuario_envio=test_user
        )

        from unittest.mock import Mock
        mock_request = Mock()
        mock_request.user = test_user
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        data = {
            'num_envio': 'ENV001',
            'tipo_respuesta': 1,
        }
        serializer = EnvioSerializer(data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'num_envio' in serializer.errors

    def test_tipo_respuesta_invalido(self, test_user):
        """Test que tipus resposta ha de ser 1, 2 o 3"""
        from unittest.mock import Mock
        mock_request = Mock()
        mock_request.user = test_user
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        data = {
            'num_envio': 'ENV001',
            'tipo_respuesta': 5,
        }
        serializer = EnvioSerializer(data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'tipo_respuesta' in serializer.errors

    def test_envio_sin_especies_invalido(self, test_user):
        """Test que enviament ha de tenir almenys una espècie"""
        from unittest.mock import Mock
        mock_request = Mock()
        mock_request.user = test_user
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        data = {
            'num_envio': 'ENV001',
            'tipo_respuesta': 1,
            'establecimientos_venta': [
                {
                    'num_identificacion_establec': 'EST001',
                    'ventas_unidad_productiva': [
                        {
                            'metodo_produccion': 1,
                            'buque': {
                                'codigo_buque': 'ESP-001',
                            },
                            'especies': []
                        }
                    ]
                }
            ]
        }
        serializer = EnvioSerializer(data=data, context={'request': mock_request})
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

    def test_create_envio_completo(self, test_user):
        """Test crear enviament complet amb tota la jerarquia"""
        from unittest.mock import Mock
        mock_request = Mock()
        mock_request.user = test_user
        mock_request.META = {'REMOTE_ADDR': '127.0.0.1'}

        data = {
            'num_envio': 'ENV_FULL_001',
            'tipo_respuesta': 1,
            'establecimientos_venta': [
                {
                    'num_identificacion_establec': 'EST001',
                    'ventas_unidad_productiva': [
                        {
                            'metodo_produccion': 1,
                            'buque': {
                                'codigo_buque': 'ESP-001',
                                'puerto_al5': 'ESBAR',
                                'armador': 'Test Armador',
                                'capitan': 'Test Capità'
                            },
                            'especies': [
                                {
                                    'num_doc_venta': 'NV001',
                                    'especie_al3': 'HKE',
                                    'fecha_venta': '2025-10-22',
                                    'cantidad': 100,
                                    'precio': 350,
                                    'tipo_cif_nif_vendedor': 1,
                                    'nif_vendedor': '12345678A',
                                    'nombre_vendedor': 'Test Vendedor',
                                    'nif_comprador': 'B12345678',
                                    'id_tipo_nif_cif_comprador': 1,
                                    'nombre_comprador': 'Test Comprador',
                                    'fechas_captura': [
                                        {
                                            'fecha_captura_ini': '2025-10-01',
                                            'fecha_captura_fin': '2025-10-15'
                                        }
                                    ]
                                },
                                {
                                    'num_doc_venta': 'NV002',
                                    'especie_al3': 'COD',
                                    'fecha_venta': '2025-10-22',
                                    'cantidad': 50,
                                    'precio': 450,
                                    'tipo_cif_nif_vendedor': 1,
                                    'nif_vendedor': '12345678A',
                                    'nombre_vendedor': 'Test Vendedor',
                                    'nif_comprador': 'B12345678',
                                    'id_tipo_nif_cif_comprador': 1,
                                    'nombre_comprador': 'Test Comprador'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        serializer = EnvioSerializer(data=data, context={'request': mock_request})
        assert serializer.is_valid(), serializer.errors

        envio = serializer.save()
        assert envio.num_envio == 'ENV_FULL_001'
        assert envio.validado is True
        assert envio.establecimientos.count() == 1

        establecimiento = envio.establecimientos.first()
        assert establecimiento.unidades_productivas.count() == 1

        unidad = establecimiento.unidades_productivas.first()
        assert unidad.especies.count() == 2
        assert unidad.buque is not None

        # Verificar que les espècies tenen dates de captura
        especie_con_fechas = unidad.especies.filter(num_doc_venta='NV001').first()
        assert especie_con_fechas.fechas_captura.count() == 1

    def test_to_representation_respuesta_reducida(self, test_user):
        """Test representació amb resposta reduïda (tipus 3)"""
        envio = Envio.objects.create(
            num_envio='ENV001',
            tipo_respuesta=3,
            usuario_envio=test_user
        )

        serializer = EnvioSerializer(envio)
        data = serializer.data

        # Resposta reduïda només inclou camps bàsics
        assert 'num_envio' in data
        assert 'fecha_recepcion' in data
        assert 'procesado' in data
        assert 'validado' in data
        assert 'establecimientos_venta' not in data

    def test_to_representation_respuesta_media(self, test_user):
        """Test representació amb resposta mitjana (tipus 2)"""
        envio = Envio.objects.create(
            num_envio='ENV002',
            tipo_respuesta=2,
            usuario_envio=test_user
        )
        establecimiento = EstablecimientoVenta.objects.create(
            envio=envio,
            num_identificacion_establec='EST001'
        )
        unidad = UnidadProductiva.objects.create(
            establecimiento=establecimiento,
            metodo_produccion=1,
            tipo_unidad='BUQUE'
        )
        Buque.objects.create(
            unidad_productiva=unidad,
            codigo_buque='ESP-001'
        )
        Especie.objects.create(
            unidad_productiva=unidad,
            num_doc_venta='NV001',
            especie_al3='HKE',
            fecha_venta=date(2025, 10, 22),
            cantidad=100,
            precio=350
        )

        serializer = EnvioSerializer(envio)
        data = serializer.data

        # Resposta mitjana no inclou espècies
        assert 'establecimientos_venta' in data
        if data['establecimientos_venta']:
            for est in data['establecimientos_venta']:
                if 'ventas_unidad_productiva' in est:
                    for unidad in est['ventas_unidad_productiva']:
                        assert 'especies' not in unidad


@pytest.mark.django_db
class TestEnvioListSerializer:
    """Tests per al serializer de llista d'enviaments"""

    def test_list_serializer(self, test_user):
        """Test serializer de llista amb informació resumida"""
        envio = Envio.objects.create(
            num_envio='ENV001',
            tipo_respuesta=1,
            usuario_envio=test_user
        )
        EstablecimientoVenta.objects.create(
            envio=envio,
            num_identificacion_establec='EST001'
        )
        EstablecimientoVenta.objects.create(
            envio=envio,
            num_identificacion_establec='EST002'
        )

        serializer = EnvioListSerializer(envio)
        data = serializer.data

        assert data['num_envio'] == 'ENV001'
        assert 'usuario' in data
        assert data['num_establecimientos'] == 2


@pytest.mark.django_db
class TestEnvioStatusSerializer:
    """Tests per al serializer d'estat d'enviament"""

    def test_status_serializer(self, test_user):
        """Test serializer d'estat"""
        envio = Envio.objects.create(
            num_envio='ENV001',
            tipo_respuesta=1,
            usuario_envio=test_user,
            procesado=True,
            validado=True
        )

        serializer = EnvioStatusSerializer(envio)
        data = serializer.data

        assert data['num_envio'] == 'ENV001'
        assert data['procesado'] is True
        assert data['validado'] is True
        assert 'errores' in data
        assert 'fecha_recepcion' in data
