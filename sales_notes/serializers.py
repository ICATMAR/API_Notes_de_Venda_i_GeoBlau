"""
Serialitzadors per l'API de notes de venda
Implementen validacions segons l'esquema JSON proporcionat
"""
from rest_framework import serializers
from .models import (
    Envio, EstablecimientoVenta, UnidadProductiva,
    Buque, Granja, PersonaFisicaJuridica,
    Especie, FechaCaptura
)
from django.db import transaction
import jsonschema
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FechaCapturaSerializer(serializers.ModelSerializer):
    """Serialitzador per dates de captura"""
    
    class Meta:
        model = FechaCaptura
        fields = ['fecha_captura_ini', 'fecha_captura_fin']
    
    def validate(self, data):
        """Validar que la data de fi sigui posterior a la d'inici"""
        if data.get('fecha_captura_fin'):
            if data['fecha_captura_fin'] < data['fecha_captura_ini']:
                raise serializers.ValidationError(
                    "La data de fi de captura no pot ser anterior a la d'inici"
                )
        return data


class EspecieSerializer(serializers.ModelSerializer):
    """Serialitzador per espècies"""
    fechas_captura = FechaCapturaSerializer(many=True, required=False)
    
    class Meta:
        model = Especie
        fields = [
            'num_doc_venta', 'especie_al3', 'zona', 'zona_geografica',
            'ccaa', 'pais_al3', 'masa_agua', 'arte_al3', 'otro_arte',
            'cod_especie_conservacion', 'cod_especie_presentacion',
            'presentacion_oth', 'id_presentacion_oth', 'cod_especie_frescura',
            'cod_especie_calibre', 'fecha_venta', 'lote', 'cod_contrato_alim',
            'num_doc_transporte', 'num_declaracion_recog', 'certificado_de_origen',
            'tipo_cif_nif_vendedor', 'nif_vendedor', 'nombre_vendedor',
            'direccion_vendedor', 'nif_comprador', 'id_tipo_nif_cif_comprador',
            'pais_comprador', 'nombre_comprador', 'direccion_comprador',
            'precio', 'cod_moneda', 'cantidad', 'num_ejemplares', 'num_cajas',
            'es_talla_reglamentaria', 'tipo_retirada', 'cod_destino_retirado',
            'lugar_almacenamiento', 'observaciones', 'num_acta_inspeccion',
            'fechas_captura'
        ]
    
    def validate_especie_al3(self, value):
        """Validar format del codi d'espècie"""
        if not value.isalpha() or len(value) != 3:
            raise serializers.ValidationError(
                "El codi d'espècie ha de ser 3 lletres (format FAO AL3)"
            )
        return value.upper()
    
    def validate_cantidad(self, value):
        """Validar que la quantitat sigui positiva"""
        if value <= 0:
            raise serializers.ValidationError(
                "La quantitat ha de ser superior a 0"
            )
        return value
    
    def validate_precio(self, value):
        """Validar que el preu sigui positiu o zero"""
        if value < 0:
            raise serializers.ValidationError(
                "El preu no pot ser negatiu"
            )
        return value
    
    def validate(self, data):
        """Validacions creuades"""
        # Si hi ha retirada, validar camps relacionats
        if data.get('tipo_retirada') and data.get('tipo_retirada') != 1:
            if not data.get('cod_destino_retirado'):
                raise serializers.ValidationError(
                    "Si hi ha retirada, cal especificar el codi de destí"
                )
        
        # Validar que si no és talla reglamentària, hi hagi informació addicional
        if not data.get('es_talla_reglamentaria', True):
            if not data.get('observaciones'):
                logger.warning(
                    f"Espècie {data.get('especie_al3')} amb talla no reglamentària sense observacions"
                )
        
        return data


class BuqueSerializer(serializers.ModelSerializer):
    """Serialitzador per vaixells"""
    
    class Meta:
        model = Buque
        fields = [
            'codigo_buque', 'puerto_al5', 'armador', 'capitan',
            'fecha_regreso_puerto', 'cod_marea'
        ]
    
    def validate_puerto_al5(self, value):
        """Validar format del codi de port"""
        if value and len(value) != 5:
            raise serializers.ValidationError(
                "El codi de port ha de tenir 5 caràcters (2 lletres + 3 alfanumèrics)"
            )
        return value.upper() if value else value


class GranjaSerializer(serializers.ModelSerializer):
    """Serialitzador per granges"""
    
    class Meta:
        model = Granja
        fields = ['codigo_rega', 'lugar_descarga', 'fecha_produccion']
    
    def validate_codigo_rega(self, value):
        """Validar longitud del codi REGA"""
        if len(value) > 14:
            raise serializers.ValidationError(
                "El codi REGA no pot superar 14 caràcters"
            )
        return value


class PersonaFisicaJuridicaSerializer(serializers.ModelSerializer):
    """Serialitzador per persones físiques/jurídiques"""
    
    class Meta:
        model = PersonaFisicaJuridica
        fields = ['nif_persona', 'lugar_descarga', 'fecha_descarga']
    
    def validate_nif_persona(self, value):
        """Validació bàsica del NIF"""
        if len(value) > 17:
            raise serializers.ValidationError(
                "El NIF no pot superar 17 caràcters"
            )
        return value.upper()


class UnidadProductivaSerializer(serializers.ModelSerializer):
    """
    Serialitzador per unitats productives amb polimorfisme
    Gestiona Buque, Granja o PersonaFisicaJuridica segons el tipus
    """
    buque = BuqueSerializer(required=False, allow_null=True)
    granja = GranjaSerializer(required=False, allow_null=True)
    persona = PersonaFisicaJuridicaSerializer(required=False, allow_null=True)
    especies = EspecieSerializer(many=True, required=False)
    
    class Meta:
        model = UnidadProductiva
        fields = ['metodo_produccion', 'tipo_unidad', 'buque', 'granja', 'persona', 'especies']
    
    def validate(self, data):
        """
        Validar que el tipus d'unitat sigui coherent amb el mètode de producció
        i que s'incloguin les dades correctes segons el tipus
        """
        metodo = data.get('metodo_produccion')
        
        # Determinar quin tipus d'unitat hauria de ser segons el mètode
        if metodo in [1, 4]:  # Pesca extractiva o aqüicultura aigües interiors
            # Pot ser Buque o Persona
            if not (data.get('buque') or data.get('persona')):
                raise serializers.ValidationError(
                    "Per mètode de producció 1 o 4, cal especificar buque o persona"
                )
        elif metodo == 2:  # Aqüicultura marina
            if not data.get('granja'):
                raise serializers.ValidationError(
                    "Per mètode de producció 2, cal especificar dades de granja"
                )
        elif metodo == 3:  # Pesca extractiva aigües interiors
            if not data.get('persona'):
                raise serializers.ValidationError(
                    "Per mètode de producció 3, cal especificar dades de persona"
                )
        
        # Validar que només hi hagi un tipus d'unitat
        tipus_presents = sum([
            bool(data.get('buque')),
            bool(data.get('granja')),
            bool(data.get('persona'))
        ])
        
        if tipus_presents != 1:
            raise serializers.ValidationError(
                "Cal especificar exactament un tipus d'unitat productiva (buque, granja o persona)"
            )
        
        # Establir el tipus d'unitat automàticament
        if data.get('buque'):
            data['tipo_unidad'] = 'BUQUE'
        elif data.get('granja'):
            data['tipo_unidad'] = 'GRANJA'
        elif data.get('persona'):
            data['tipo_unidad'] = 'PERSONA'
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """Crear unitat productiva amb les seves dades específiques"""
        # Extreure dades específiques
        buque_data = validated_data.pop('buque', None)
        granja_data = validated_data.pop('granja', None)
        persona_data = validated_data.pop('persona', None)
        especies_data = validated_data.pop('especies', [])
        
        # Crear la unitat productiva
        unidad = UnidadProductiva.objects.create(**validated_data)
        
        # Crear el tipus específic
        if buque_data:
            Buque.objects.create(unidad_productiva=unidad, **buque_data)
        elif granja_data:
            Granja.objects.create(unidad_productiva=unidad, **granja_data)
        elif persona_data:
            PersonaFisicaJuridica.objects.create(unidad_productiva=unidad, **persona_data)
        
        # Crear espècies
        for especie_data in especies_data:
            fechas_captura_data = especie_data.pop('fechas_captura', [])
            especie = Especie.objects.create(unidad_productiva=unidad, **especie_data)
            
            for fecha_data in fechas_captura_data:
                FechaCaptura.objects.create(especie=especie, **fecha_data)
        
        return unidad

"""
Serialitzadors principals per Envio i EstablecimientoVenta
"""
from rest_framework import serializers
from .models import Envio, EstablecimientoVenta
from .serializers import UnidadProductivaSerializer
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class EstablecimientoVentaSerializer(serializers.ModelSerializer):
    """Serialitzador per establiments de venda"""
    ventas_unidad_productiva = UnidadProductivaSerializer(
        many=True,
        source='unidades_productivas',
        required=False
    )
    
    class Meta:
        model = EstablecimientoVenta
        fields = ['num_identificacion_establec', 'ventas_unidad_productiva']
    
    def validate_num_identificacion_establec(self, value):
        """Validar identificació de l'establiment"""
        if not value or len(value) == 0:
            raise serializers.ValidationError(
                "El número d'identificació de l'establiment és obligatori"
            )
        return value


class EnvioSerializer(serializers.ModelSerializer):
    """
    Serialitzador principal per l'enviament de notes de venda
    Gestiona tota la jerarquia de dades
    """
    establecimientos_venta = EstablecimientoVentaSerializer(
        many=True,
        source='establecimientos',
        required=False
    )
    
    class Meta:
        model = Envio
        fields = [
            'id', 'num_envio', 'tipo_respuesta', 'fecha_recepcion',
            'procesado', 'validado', 'errores', 'establecimientos_venta'
        ]
        read_only_fields = ['id', 'fecha_recepcion', 'procesado', 'validado', 'errores']
    
    def validate_num_envio(self, value):
        """Validar que el número d'enviament sigui únic"""
        if Envio.objects.filter(num_envio=value).exists():
            raise serializers.ValidationError(
                f"Ja existeix un enviament amb el número {value}"
            )
        return value
    
    def validate_tipo_respuesta(self, value):
        """Validar tipus de resposta"""
        if value not in [1, 2, 3]:
            raise serializers.ValidationError(
                "El tipus de resposta ha de ser 1 (Completa), 2 (Mitjana) o 3 (Reduïda)"
            )
        return value
    
    def validate(self, data):
        """Validacions a nivell d'enviament"""
        establecimientos = data.get('establecimientos', [])
        
        if not establecimientos:
            logger.warning(
                f"Enviament {data.get('num_envio')} sense establiments de venda"
            )
        
        # Validar que hi hagi almenys una unitat productiva amb espècies
        total_especies = 0
        for establecimiento in establecimientos:
            unidades = establecimiento.get('unidades_productivas', [])
            for unidad in unidades:
                especies = unidad.get('especies', [])
                total_especies += len(especies)
        
        if total_especies == 0:
            raise serializers.ValidationError(
                "L'enviament ha de contenir almenys una espècie"
            )
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Crear enviament amb tota la jerarquia de dades
        Utilitza transacció per garantir atomicitat
        """
        establecimientos_data = validated_data.pop('establecimientos', [])
        
        # Obtenir l'usuari del context
        user = self.context['request'].user
        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        
        # Crear l'enviament
        envio = Envio.objects.create(
            usuario_envio=user,
            ip_origen=ip_address,
            **validated_data
        )
        
        logger.info(
            f"Creant enviament {envio.num_envio} per usuari {user.username}"
        )
        
        # Crear establiments i tota la jerarquia
        try:
            for establecimiento_data in establecimientos_data:
                unidades_data = establecimiento_data.pop('unidades_productivas', [])
                
                establecimiento = EstablecimientoVenta.objects.create(
                    envio=envio,
                    **establecimiento_data
                )
                
                # Crear unitats productives (que a la vegada creen buque/granja/persona i espècies)
                for unidad_data in unidades_data:
                    serializer = UnidadProductivaSerializer(data=unidad_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(establecimiento=establecimiento)
            
            # Marcar com a validat si tot ha anat bé
            envio.validado = True
            envio.save()
            
            logger.info(
                f"Enviament {envio.num_envio} creat correctament amb "
                f"{envio.establecimientos.count()} establiments"
            )
            
        except Exception as e:
            logger.error(
                f"Error creant enviament {envio.num_envio}: {str(e)}",
                exc_info=True
            )
            # Afegir error a l'enviament
            envio.errores.append({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            envio.validado = False
            envio.save()
            raise
        
        return envio
    
    def to_representation(self, instance):
        """
        Personalitzar la representació de sortida
        Segons el tipo_respuesta, retornar més o menys informació
        """
        representation = super().to_representation(instance)
        
        tipo_respuesta = instance.tipo_respuesta
        
        if tipo_respuesta == 3:  # Resposta reduïda
            # Només retornar informació bàsica
            return {
                'num_envio': representation['num_envio'],
                'fecha_recepcion': representation['fecha_recepcion'],
                'procesado': representation['procesado'],
                'validado': representation['validado']
            }
        elif tipo_respuesta == 2:  # Resposta mitjana
            # Retornar sense detalls d'espècies
            if 'establecimientos_venta' in representation:
                for est in representation['establecimientos_venta']:
                    if 'ventas_unidad_productiva' in est:
                        for unidad in est['ventas_unidad_productiva']:
                            unidad.pop('especies', None)
        
        # tipo_respuesta == 1: Resposta completa (per defecte)
        return representation


class EnvioListSerializer(serializers.ModelSerializer):
    """Serialitzador lleuger per llistar enviaments"""
    usuario = serializers.StringRelatedField(source='usuario_envio')
    num_establecimientos = serializers.IntegerField(
        source='establecimientos.count',
        read_only=True
    )
    
    class Meta:
        model = Envio
        fields = [
            'id', 'num_envio', 'tipo_respuesta',
            'fecha_recepcion', 'procesado', 'validado',
            'usuario', 'num_establecimientos'
        ]
        read_only_fields = fields


class EnvioStatusSerializer(serializers.ModelSerializer):
    """Serialitzador per consultar l'estat d'un enviament"""
    
    class Meta:
        model = Envio
        fields = [
            'num_envio', 'fecha_recepcion', 'procesado',
            'fecha_procesado', 'validado', 'errores'
        ]
        read_only_fields = fields


# Importar datetime per les validacions
from datetime import datetime